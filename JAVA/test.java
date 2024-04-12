public static long twoDimensions(List<String> list, int n) {
    long res = 0;
    int rowCount =0,colCount=0;
    for(int i=0;i<n;i++)
    {
        int row = list.get(i).charAt(0) - 48;
        int col = list.get(i).charAt(2) - 48;
        if(row > rowCount)
            rowCount = row;
        if(col >colCount)
            colCount = col;
    }
    int tempArr[][] = new int[rowCount+1][colCount+1];
    for(int i = 0;i<n;i++)
    {
        int row = list.get(i).charAt(0) - 48;
        int col = list.get(i).charAt(2) - 48;
        for(int j=row;j>=1;j--)
        {
            int m = j;
        for(int k=1;k<=col;k++)
        {
            tempArr[m][k]= tempArr[m][k]+1;
            if(tempArr[m][k]>res)
                res = tempArr[m][k];
        }
        }
        System.out.println("for row: "+row+" col: "+col);
        for(int j = 0;j<=rowCount;j++)
        {
            for(int k=0;k<=colCount;k++)
            {
                System.out.print(""+tempArr[j][k]);
            }
            System.out.println("");
        }
        System.out.println("");
    }
    return res;
    }


