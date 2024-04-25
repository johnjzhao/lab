#include <iostream>
#include <vector>
#include <unordered_map>

using namespace std;

int priceCheck(int products_count, const char** products, int productPrices_count, float* productPrices, int productSold_count, const char** productSold, int soldPrice_count, float* soldPrice) {
    int errors = 0;
    unordered_map<string, float> productMap;

    for (int i = 0; i < products_count; i++) {
        productMap[products[i]] = productPrices[i];
    }

    for (int i = 0; i < productSold_count; i++) {
        if (productMap[productSold[i]] != soldPrice[i]) {
            errors++;
        }
    }

    return errors;
}

int main() {
    const char *products[] = {"eggs", "milk", "cheese"};
    int products_count = sizeof(products)/sizeof(products[0]);
    float productPrices[] = {2.89, 3.29, 5.79};
    int productPrices_count = sizeof(productPrices)/sizeof(productPrices[0]);
    const char *productSold[] = {"eggs", "eggs", "cheese", "milk"};
    int productSold_count = sizeof(productSold)/sizeof(productSold[0]);
    float soldPrice[] = {2.89, 2.99, 5.97, 3.29};
    int soldPrice_count = sizeof(soldPrice)/sizeof(soldPrice[0]);

    int errorCount = priceCheck(products_count, products, productPrices_count, productPrices, productSold_count, productSold, soldPrice_count, soldPrice);
    cout << "Number of errors: " << errorCount << endl;


    return 0;
}
