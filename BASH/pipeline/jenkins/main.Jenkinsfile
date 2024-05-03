/*** VARIABLES ***/
def nowDate = new Date().format("yyyy-MM-dd", TimeZone.getTimeZone('EST'))
def nowTime = new Date().format("HH:mm:ss", TimeZone.getTimeZone('EST'))
def SKIP_REMAINING_STAGES = false
String uuid = UUID.randomUUID().toString()
/*** ***/

/*** PIPELINE ***/
pipeline {
    agent {
        kubernetes {
            cloud "tdv-superpipeline-openshift-devops1"
            label "tdv-superpipeline-${uuid}"
            customWorkspace "/home/jenkins/agent/workspace"
            defaultContainer "jnlp"
            yamlFile 'jenkins/KubernetesPod.yaml'
        }
    }
    options { disableConcurrentBuilds() }
    parameters {
        booleanParam(name: 'IGNORE_RULES_ENGINE_ERRORS', defaultValue: false, description: 'Ignore rules engine errors (pipeline will continue).')
        booleanParam(name: 'FORCE_RULES_ENGINE', defaultValue: true, description: 'Disregard checks and force running of Rules Engine.')
        booleanParam(name: 'FORCE_DDL_DEPLOY', defaultValue: true, description: 'Disregard checks and force DDL deployment.')
        booleanParam(name: 'IGNORE_FAILED_TESTS', defaultValue: false, description: 'Ignore failed unittests (pipeline will continue).')
        booleanParam(name: 'FORCE_ETL_DEPLOY', defaultValue: true, description: 'Disregard checks and force ETL (DML & DAG) deployment.')
        booleanParam(name: 'REVERT_LAST_MERGE_REQUEST', defaultValue: false, description: 'Revert last merge request for test, release and main branches')
    }
    environment {
        GITHUB_TOKEN_CREDS_ID=configValues('GITHUB_TOKEN_CREDS_ID')
        GITHUB_TOKEN = credentials("${GITHUB_TOKEN_CREDS_ID}")
        JENKINS_CREDS_ID=configValues('JENKINS_CREDS_ID')
        JENKINS_CREDS = credentials("${JENKINS_CREDS_ID}")
        CX_CREDENTIALS_ID=configValues('CX_CREDENTIALS_ID')
        CX_CREDENTIALS = credentials("${CX_CREDENTIALS_ID}")
        WEBHOOK_GITHUB_TOKEN_ID=configValues('WEBHOOK_GITHUB_TOKEN_ID')
        WEBHOOK_GITHUB_TOKEN = credentials("${WEBHOOK_GITHUB_TOKEN_ID}")
      }

    stages{
        stage("Environment Setup"){
            steps{
                script {
                    def configData = readYaml file: 'jenkins/config.yaml'
                    configData["COMMON"].each { key, value ->
                    env."${key}" = value
                    echo env."${key}"
                    }
                    if (env.DDL_PROJECT_NAME == null || env.DDL_PROJECT_NAME.isEmpty()) {
                        error("DDL_PROJECT_NAME environment variable is missing.")

                    }
                                      
                    // Clean string variables for compatibility in image tags, k8s job names, etc.
                    env.DDL_PROJECT_NAME_CLEAN = env.DDL_PROJECT_NAME.replaceAll(/[^a-zA-Z0-9]/, '-').toLowerCase()
                    env.BRANCH_NAME_CLEAN = env.BRANCH_NAME.replaceAll(/[^a-zA-Z0-9]/, '-').toLowerCase()

                    // Job name utilized for image tagging, k8s job names, etc.
                    env.JOB_NAME = "${env.DDL_PROJECT_NAME_CLEAN}-${env.BRANCH_NAME_CLEAN}"

                    env.DDL_DIR = env.DDL_DIR != null && !env.DDL_DIR.isEmpty() ? env.DDL_DIR : 'ddl/'
                    env.TEST_FT_DIR = env.TEST_FT_DIR != null && !env.TEST_FT_DIR.isEmpty() ? env.TEST_FT_DIR : 'tests/features/'
                    env.GIT_REPO_NAME = env.GIT_URL.replaceFirst(/^.*\/([^\/]+?).git$/, '$1')
              
                    def branchName =  env.BRANCH_NAME
                    if(branchName.startsWith("feature")){
                        configData["DEV"].each { key, value ->
                        env."${key}" = value
                        echo env."${key}"
                       }
                    }

                    if(branchName == 'test') {
                        configData["TEST"].each { key, value ->
                        env."${key}" = value
                        echo env."${key}"
                       }
                    }
                    
                    if(branchName == "release") {
                        configData["PROD"].each { key, value ->
                        env."${key}" = value
                        echo env."${key}"
                       }
                    }
                    
                    if(branchName == 'master' || branchName == 'main') {
                        SKIP_REMAINING_STAGES = true
                        echo "Skipping remaining deployment stages for main branch as release branch was deployed into production"
                    }
                }
            }
        }

        stage( "Validation: PR Check"){
            when {
                expression { return env.JOB_BASE_NAME.startsWith('PR-') }
            }
            steps {
               script {
                    env.GREP_RETURN_CODE=0
                    sh '''
                        curl -o pr.json "https://sunvalle:${WEBHOOK_GITHUB_TOKEN_PSW}@github.sys.sunvalle.com/api/v3/repos/sunvalle/${GIT_REPO_NAME}/pulls?base=release"
                        #cat pr.json
                    '''
                   def json = readJSON file: 'pr.json'
                   def prNums = json.collect{it['number']}
                   def currentPRNUM = env.JOB_BASE_NAME.replace('PR-', '')
                   SKIP_REMAINING_STAGES = true
                   echo "Current PR-Number : ${currentPRNUM}"
                   echo " PR_Number : ${prNums}"
                   if ( "${prNums}".contains("${currentPRNUM}") ) {
                        env.pr="${currentPRNUM}"
                        echo "${pr}"
                        sh '''
                           set +x
                           curl -X POST "https://${JENKINS_CREDS_USR}:${JENKINS_CREDS_PSW}@orchestrator1.orchestrator-v2.sys.sunvalle.com/job/orchestrators-folders/job/enterprise360/job/360-data-services/job/TDV/job/TDV-Utilities/job/PR-Checks/job/master/buildWithParameters?GIT_REPO_NAME=${GIT_REPO_NAME}&PR_Number=${pr}&delay=0sec"
                           while [ $GREP_RETURN_CODE -eq 0 ]
                           do
                              sleep 7
                              curl --silent https://${JENKINS_CREDS_USR}:${JENKINS_CREDS_PSW}@orchestrator1.orchestrator-v2.sys.sunvalle.com/job/orchestrators-folders/job/enterprise360/job/360-data-services/job/TDV/job/TDV-Utilities/job/PR-Checks/job/master/lastBuild/api/json | grep result\\":null > /dev/null || if [ $? -eq 1 ]; then BUILD_STATUS=$(curl --silent https://${JENKINS_CREDS_USR}:${JENKINS_CREDS_PSW}@orchestrator1.orchestrator-v2.sys.sunvalle.com/job/orchestrators-folders/job/enterprise360/job/360-data-services/job/TDV/job/TDV-Utilities/job/PR-Checks/job/master/lastBuild/api/json | grep -o '"result": *"[^"]*"' | grep -o '"[^"]*"$' | sed -e 's/^"//' -e 's/"$//')
                              ID=$(curl --silent https://${JENKINS_CREDS_USR}:${JENKINS_CREDS_PSW}@orchestrator1.orchestrator-v2.sys.sunvalle.com/job/orchestrators-folders/job/enterprise360/job/360-data-services/job/TDV/job/TDV-Utilities/job/PR-Checks/job/master/lastBuild/api/json | grep -o '"id": *"[^"]*"' | grep -o '"[^"]*"$' | sed -e 's/^"//' -e 's/"$//')
                              echo " PR-Checks Jenkins JOB URL : https://orchestrator1.orchestrator-v2.sys.sunvalle.com/job/orchestrators-folders/job/enterprise360/job/360-data-services/job/TDV/job/TDV-Utilities/job/PR-Checks/job/master/${ID}"
                              if [ $BUILD_STATUS == 'SUCCESS' ]
                               then
                                  echo 'PR Check Job Success, Valid pull request'
                                  echo ''
                                  exit 0
                              elif [ $BUILD_STATUS == 'ABORTED' ]
                               then
                                  echo 'PR Check Job Aborted'
                                  exit 1
                              else
                                  echo 'PR Check Job Failed'
                                  exit 1
                              fi
                                  exit 0
                              fi

                              GREP_RETURN_CODE=$?
                            done
                            '''

                    }
                }
            }
        }

        stage("Revert last merge request for test, release and and main branches") {
            when {
                expression { return params.REVERT_LAST_MERGE_REQUEST }
            }
            steps{
                script {
                    SKIP_REMAINING_STAGES = true
                    env.PROJECT_GIT_URL_WITH_USER_PWD = "${GIT_URL}".replace("https://", "https://${GITHUB_TOKEN_USR}:${GITHUB_TOKEN_PSW}@")
                    echo "${PROJECT_GIT_URL_WITH_USER_PWD}"
                    if (env.BRANCH_NAME == 'main' || env.BRANCH_NAME == 'test' || env.BRANCH_NAME == "release") {
                        echo "Reverting last merge as deployment failed"
                        sh"""
                            git log --merges
                            git config --global user.email "TDV_PIPELINE_ADMIN@Cigna.com"
                            git config --global user.name "TDV_PIPELINE_ADMIN"
                            git checkout ${env.BRANCH_NAME}
                            git revert HEAD -m 1
                            git push -u ${PROJECT_GIT_URL_WITH_USER_PWD} ${env.BRANCH_NAME}
                        """
                    }
                }
            }
        }

        stage("Validation: Checkmarx Scanning"){
            when {
                expression { return !SKIP_REMAINING_STAGES }
            } 
            steps{
                container('cx-toolshack'){ 
                    script{
                        sh '''
                            java -jar /cxtools/CLI/CxConsolePlugin-CLI-1.1.9.jar Scan -v \
                            -CxServer "https://sunvalle.checkmarx.net" \
                            -ProjectName "${CX_PROJECT_PATH}${CX_TEAM}/${CX_PROJECT_NAME}" \
                            -CxUser $CX_CREDENTIALS_USR \
                            -CxPassword $CX_CREDENTIALS_PSW \
                            -LocationType folder \
                            -LocationPath . \
                            -LocationPathExclude "tests/,jenkins/" \
                            -Configuration "Multi-Language Scan" \
                            -scahigh 5 \
                            -ReportPDF results.pdf \
                        '''
                        // To DO: Fail this stage when there are high severity issues > 5

                        emailext subject: "Checkmarx Scan Result for Project: ${CX_PROJECT_NAME}",
                        body: "Attached is your Checkmarx scan result, and summary output file. Flaws identified as Very-High or High, must be addressed immediately.",
                        attachmentsPattern: '**/results.pdf',
                        to: "${env.TEAM_EMAIL_ID}"
                    }
                }
            }
        }

        // To Do: Differentaite between oss and ccw rules engine based on dataset variable
        stage("DDL: Run Rules Engine"){
            when {
                allOf { 
                    expression { return !SKIP_REMAINING_STAGES }
                    anyOf {
                        expression { return env.BRANCH_NAME == 'test' || env.BRANCH_NAME == "release"}
                        expression { return params.FORCE_RULES_ENGINE }
                        expression { return params.FORCE_DDL_DEPLOY }
                        changeset pattern: "ddl/**/*", comparator: "GLOB"

                    } 
                }
            }
            steps {
                script {
                    try {
                        container('rules-engine') {
                            sh """
                                # Copy ddl to rules engine target dir
                                mkdir -p /app/RulesEngine/Teradata/src/
                                cp -R ddl/. /app/RulesEngine/Teradata/src/

                                # Rename changelog xml file to rules engine target
                                cp /app/RulesEngine/Teradata/src/${env.CHANGELOG_FILE} /app/RulesEngine/Teradata/src/update.xml

                                cat /app/RulesEngine/Teradata/src/update.xml
                                ls -R /app/RulesEngine/Teradata/src/

                                # Run rules engine
                                /app/RE_Run_Commands.sh

                                # Check RE exit code
                                (cat Rules_Engine.log | grep 'Returning exit code 0') || exit 1
                            """
                        }
                    }
                    catch (Exception e) {
                        script {
                            if (params.IGNORE_RULES_ENGINE_ERRORS) {
                                echo "RULES ENGINE ERRORS - Ignoring Rule Engine errors (IGNORE_RULE_ENGINE_ERRORS=true)."
                            }
                            else {
                                error("RULES ENGINE ERRORS")

                            }
                        }
                    }
                }
            }
        }

        stage("DDL: Deploy & Run Liquibase"){
            when { 
                allOf {
                    expression { return !SKIP_REMAINING_STAGES }
                    anyOf {
                        expression { return env.BRANCH_NAME == 'test' ||  env.BRANCH_NAME == "release"}
                        expression { return params.FORCE_DDL_DEPLOY }
                        changeset pattern: "ddl/**/*", comparator: "GLOB"
                    }
                }
            }
            steps {
                script {
                    echo "Federating to AWS"
                    aws_fed()

                    echo "Preparing liquibase docker build directory with DDL files in ${env.DDL_DIR}"
                    // Copy files from DDL_DIR into liquibase directory
                    sh  "${WORKSPACE}/scripts/build-liquibase-dir.sh -d ${env.DDL_DIR}"

                    echo "Building & pushing image..."

                    def image_name = "${env.ECR_TDV_LIQUIBASE}:${env.JOB_NAME}"
                    echo "Image name: ${image_name}"

                    container('kaniko') {
                        def ACCOUNT_NUMBER = env.AWS_FED_ACCOUNT
                        sh  """
                            #!/busybox/sh -ex
                            echo "{\\"credStore\\": \\"ecr-login\\"}" > /kaniko/.docker/config.json
                            /kaniko/executor \
                                --context ${WORKSPACE}/liquibase --cache=true \
                                --cache-repo=${ACCOUNT_NUMBER}.dkr.ecr.us-east-1.amazonaws.com/dna-ad/${ECR_TDV_LIQUIBASE} \
                                --dockerfile ${WORKSPACE}/liquibase/Dockerfile --destination ${ACCOUNT_NUMBER}.dkr.ecr.us-east-1.amazonaws.com/dna-ad/${image_name} \
                                --build-arg AWS_ACCOUNT=${ACCOUNT_NUMBER}
                            """
                    }

                    echo "Deploying to kubernetes..."

                    // Create unique JOB ID
                    env.JOB_ID = "${JOB_NAME}-${env.BUILD_NUMBER}"
                    env.DATA_ORG = env.DDL_PROJECT_NAME_CLEAN
                    echo "JOB_ID = ${env.JOB_ID}"

                    container('toolkit') {
                        withCredentials([
                        usernamePassword(credentialsId: TDV_LIQ_CRED, usernameVariable: 'TDV_LIQ_USR', passwordVariable: 'TDV_LIQ_PSW')
                        ]) {
                            sh  """
                                ### Configure kubectl ###
                                aws eks update-kubeconfig --name ${env.K8S_NAME}
                                kubectl config set-context --current --namespace=${env.K8S_NAMESPACE}

                                ### Setup k8s scripts directory ###
                                chmod 777 -R $WORKSPACE/liquibase/kubernetes/
                                mkdir -p /opt/k8s/scripts
                                cp -r $WORKSPACE/liquibase/kubernetes/$ENV/. /opt/k8s/scripts
                                cd /opt/k8s/scripts

                                ### Create env file for reference/use in deployment script ###
                                set +x
                                echo "TDV_LIQ_USR=${TDV_LIQ_USR}" > ./env.conf
                                echo "TDV_LIQ_PSW=${TDV_LIQ_PSW}" >> ./env.conf
                                set -x

                                ### Execute deployment ###
                                ./kubectl-deploy-commands.conf

                                """
                        }
                    }
                }
            }
        }

        stage ("Run Unit Tests") { 
            when {
                expression {
		            return env.BRANCH_NAME.startsWith('feature') || env.BRANCH_NAME.startsWith('test'); // Run unittesting stage only if feature branch or test branch
                }
            }
            steps {
                script {
                    try {
                        echo "Federating to AWS"
                        aws_fed()

                        echo "Preparing unittesting docker build directory with testing files in ${TEST_FT_DIR}"
                        echo "Building & pushing image..."

                        def image_name = "${env.ECR_TDV_UNITTESTING}:${env.JOB_NAME}-${env.BUILD_NUMBER}"
                        echo "Unittest Image name: ${image_name}"

                        container('kaniko') {
                            def ACCOUNT_NUMBER = env.AWS_FED_ACCOUNT
                            sh  """
                                #!/busybox/sh -ex
                                echo "{\\"credStore\\": \\"ecr-login\\"}" > /kaniko/.docker/config.json
                                /kaniko/executor \
                                    --context ${WORKSPACE}/tests --cache=true \
                                    --cache-repo=${ACCOUNT_NUMBER}.dkr.ecr.us-east-1.amazonaws.com/dna-ad/${ECR_TDV_UNITTESTING} \
                                    --dockerfile ${WORKSPACE}/tests/Dockerfile --destination ${ACCOUNT_NUMBER}.dkr.ecr.us-east-1.amazonaws.com/dna-ad/${image_name} \
                                    --build-arg AWS_ACCOUNT=${ACCOUNT_NUMBER}
                                """
                        }

                        echo "Deploying to kubernetes..."

                        // Create unique JOB ID
                        env.JOB_ID = "${JOB_NAME}-${env.BUILD_NUMBER}"
                        env.DATA_ORG = env.DDL_PROJECT_NAME_CLEAN
                        echo "JOB_ID = ${env.JOB_ID}"


                        container('toolkit') {
                            withCredentials([
                                usernamePassword(credentialsId: env.TDV_UNITTEST_SA, usernameVariable: 'TDV_UNITTEST_USR', passwordVariable: 'TDV_UNITTEST_PSW')
                            ]) {
                                sh  """
                                    echo "set namespace"
                                    ### Configure kubectl ###
                                    aws eks update-kubeconfig --name ${env.K8S_NAME}
                                    kubectl config set-context --current --namespace=${env.K8S_NAMESPACE}

                                    echo "set up kubernetes directory"

                                    ### Setup kubernetes directory ###
                                    chmod 777 -R $WORKSPACE/tests/kubernetes
                                    mkdir -p /tests/kubernetes
                                    cp -r $WORKSPACE/tests/kubernetes/. /tests/kubernetes
                                    cd /tests/kubernetes

                                    echo "create env file with secrets"

                                    ### Create env file for reference/use in deployment script ###
                                    set +x
                                    echo "TDV_UNITTEST_USR=${TDV_UNITTEST_USR}" > ./env.conf
                                    echo "TDV_UNITTEST_PSW=${TDV_UNITTEST_PSW}" >> ./env.conf
                                    set -x

                                    echo "execute deployment"

                                    ### Execute deployment ###
                                    ./kubectl-deploy-commands.conf

                                    """
                            }
                        }
                    }
                    catch (Exception e) { 
                        script {
                            if (params.IGNORE_FAILED_TESTS) {
                                echo "FAILED UNITTESTING STAGE - Ignoring failure (IGNORE_FAILED_TESTS=true)."
                            }
                            else {
                                error e.getMessage()
                            }
                        }
                    }
                }
            }
        }

        stage("ETL: DAG File Validation"){
            when {
                allOf {
                    expression { return !SKIP_REMAINING_STAGES }
                    anyOf {
                        expression { return params.FORCE_ETL_DEPLOY }
                        allOf {
                            changeset pattern: "dags/**/*", comparator: "GLOB"
                        }
                    } 
                }  
            }
            steps {
                sh '''
                #!/bin/bash
                set +x
                cd dags
                list=()
                for filepath in `find . -maxdepth 1 -name "*.py" -type f`
                do
                    filename=$(basename $filepath)
                    #echo "$filename"
                    #Length of Git-Repo-Name
                    substr=$(echo $filename | cut -c 1-${#GIT_REPO_NAME})
                    if [ "$substr" != "$GIT_REPO_NAME" ]
                    then
                        list+=($filename)
                    fi
                done
                if [ ${#list[@]} -eq 0 ]
                then
                    echo "Files name starts with $GIT_REPO_NAME "
                else
                    echo "Below files name doesn't starts with $GIT_REPO_NAME"
                    echo "${list[@]}"
                    exit 1
                fi
                '''
            }
        }

        stage("ETL: Deploy DML & DAGs"){
            when { 
                allOf {
                    expression { return !SKIP_REMAINING_STAGES }
                    anyOf {
                        expression { return params.FORCE_ETL_DEPLOY }
                        expression { return env.BRANCH_NAME == 'test' || env.BRANCH_NAME == "release"}
                        changeset pattern: "dml/**/*", comparator: "GLOB"
                        changeset pattern: "dags/**/*", comparator: "GLOB"
                        changeset pattern: "scripts/**/*", comparator: "GLOB"
                        changeset pattern: "dags/local.yaml", comparator: "GLOB"
                        changeset pattern: "dml/local.yaml", comparator: "GLOB"
                        changeset pattern: "scripts/local.yaml", comparator: "GLOB"
                    }
                }
            }
            steps {
                echo "Federating to AWS"
                aws_fed()

                container('toolkit') {
                    script {
                        if (env.BRANCH_NAME.startsWith("feature")){
                            status_code = deploy_etl(env.ENV.toLowerCase())
                            if(status_code == 1) {
                                error("ETL  DEPLOYMENTS ERRORS")
                            }
                        } else if (env.BRANCH_NAME.equals("test") || env.BRANCH_NAME == "release"){
                            sh """
                                aws s3  sync --profile=saml $WORKSPACE/dml s3://$GLUE_S3_BUCKET/$GIT_REPO_NAME/dml/
                                aws s3  sync --profile=saml $WORKSPACE/scripts s3://$GLUE_S3_BUCKET/$GIT_REPO_NAME/scripts/
                                aws s3  sync --profile=saml $WORKSPACE/dags s3://$MWAA_BUCKET/airflow/dags/
                            """
                        } else {
                            error "Error : unknown branch to deploy!"
                        }
                    }
                }
            }
        }
    }
    post {
        always {
            script {
                def endDate = new Date().format('yyyy-MM-dd', TimeZone.getTimeZone('EST'))
                def endTime = new Date().format('HH:mm:ss', TimeZone.getTimeZone('EST'))
                if (env.BRANCH_NAME == "release") {
                        sh """
                            curl -X POST "https://${JENKINS_CREDS_USR}:${JENKINS_CREDS_PSW}@orchestrator1.orchestrator-v2.sys.sunvalle.com/job/orchestrators-folders/job/enterprise360/job/360-data-services/job/TDV/job/TDV-Utilities/job/sox-compliance/job/master/buildWithParameters?ENVIRONMENT_TYPE=${ENV}&JOB_BUILD_URL=${BUILD_URL}&GIT_REPO=${GIT_REPO_NAME}&BUILD_NUM=${BUILD_NUMBER}&JOB_START_TIME=${nowDate}%20${nowTime}&JOB_END_TIME=${endDate}%20${endTime}&BRANCH=${BRANCH_NAME}&delay=0sec"
                            
                        """
                }
            }

        }
        failure {
                emailext subject: "Deployment - FAILURE - ${env.GIT_REPO_NAME}", from: 'TDV_PIPELINE_ADMIN@Cigna.com', to: "${env.TEAM_EMAIL_ID}", body: "Deployment Job Failed!\n\nGit Repo: ${env.GIT_URL}\n\nJenkins Job URL: ${env.BUILD_URL}"
        }
        aborted {
            emailext subject: "Deployment - ABORTED - ${env.GIT_REPO_NAME}",from: 'TDV_PIPELINE_ADMIN@Cigna.com', to: "${env.TEAM_EMAIL_ID}", body: "Deployment Job Aborted!\n\nGit Repo: ${env.GIT_URL}\n\nJenkins Job URL: ${env.BUILD_URL}"
        }
        success {
            emailext subject: "Deployment - SUCCESS - ${env.GIT_REPO_NAME}",from: 'TDV_PIPELINE_ADMIN@Cigna.com', to: "${env.TEAM_EMAIL_ID}", body: "Deployment Job Successful!\n\nGit Repo: ${env.GIT_URL}\n\nJenkins Job URL: ${env.BUILD_URL}"
        }
    }
}
/*** ***/



/*** FUNCTIONS ***/
//deploy to tdv
def deploy_etl(env_type) {
    println "########################################################################################################"

    def dags_text = readFile(file: "${WORKSPACE}/dags/local.yaml")
    def dags_txt_values = dags_text.split("\n")
    def file_not_exists = false
    def dag_files_list = []
    for (int i = 0 ; i < dags_txt_values.length ; i++) {
        line_value = dags_txt_values[i].trim()
        if(line_value == ""){
            continue
        }
        def filepath = "dags/${line_value}"
        def exists = fileExists filepath
        if (!exists) {
            echo "${filepath} does not exist"
            file_not_exists = true
        }
        def s3_cmd = "aws s3 cp --profile=saml $WORKSPACE/${filepath} s3://$MWAA_BUCKET/airflow/${filepath}"
        dag_files_list.add(s3_cmd)       
    }

    

    def dml_text = readFile(file: "${WORKSPACE}/dml/local.yaml")
    def dml_txt_values = dml_text.split("\n")
    def dml_files_list = []
    for (int i = 0 ; i < dml_txt_values.length ; i++) {
        line_value = dml_txt_values[i].trim()
        if(line_value == ""){
            continue
        }
        def filepath = "dml/${line_value}"
        def exists = fileExists filepath
        if (!exists) {
            echo "${filepath} does not exist"
            file_not_exists = true
        }  
        def dml_cmd = "aws s3 cp --profile=saml $WORKSPACE/${filepath} s3://$GLUE_S3_BUCKET/$GIT_REPO_NAME/${filepath}"
        dml_files_list.add(dml_cmd)
    }
    
    def scripts_text = readFile(file: "${WORKSPACE}/scripts/local.yaml")
    def scripts_txt_values = scripts_text.split("\n")
    def script_files_list = []
    for (int i = 0 ; i < scripts_txt_values.length ; i++) {
        line_value = scripts_txt_values[i].trim()
        if(line_value == ""){
            continue
        }
        def filepath = "scripts/${line_value}"
        def exists = fileExists filepath
        if (!exists) {
            echo "${filepath} does not exist"
            file_not_exists = true
        }
        def script_s3_cmd = "aws s3 cp --profile=saml $WORKSPACE/${filepath} s3://$GLUE_S3_BUCKET/$GIT_REPO_NAME/${filepath}"
        script_files_list.add(script_s3_cmd)


    }

    if(file_not_exists) {
        echo "Exiting as there are  incorrect file paths!"
        return 1
    }

    echo "INFO! Deploying dags"
    for (int i = 0 ; i < dag_files_list.size() ; i++) {
        s3_cmd = dag_files_list[i]
        sh """
          ${s3_cmd}
        """
    }

    echo "INFO! Deploying dml folders"
    for (int i = 0 ; i < dml_files_list.size() ; i++) {
        s3_cmd = dml_files_list[i]
        sh """
          ${s3_cmd}
        """
    }

    echo "INFO! Deploying script files"
    for (int i = 0 ; i < script_files_list.size() ; i++) {
        s3_cmd = script_files_list[i]
        sh """
          ${s3_cmd}
        """
    }
    return 0
    println "########################################################################################################"
}

def aws_fed() {
    container('toolkit') {
        withCredentials([usernamePassword(credentialsId: AWS_FED_CRED, usernameVariable: 'AWS_FED_SA', passwordVariable: 'AWS_FED_PASSWORD')]) {
            sh  """
                set +x
                export AWS_FED_USERNAME=${AWS_FED_SA}
                export AWS_FED_PASSWORD=${AWS_FED_PASSWORD}
                export AWS_FED_ACCOUNT=${AWS_FED_ACCOUNT}
                export AWS_FED_PROFILE=saml
                export AWS_FED_ROLENAME=${AWS_FED_ROLENAME}
                aws-fed login
            """
        }
    }
}

def configValues(x){
  def data = readYaml (file: 'jenkins/config.yaml')
  valuesYaml = data["COMMON"]
  return valuesYaml[x];
}
/*** ***/
