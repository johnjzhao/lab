from typing import List

def priceCheck(products: List[str], productPrices: List[float], productSold: List[str], soldPrice: List[float]) -> int:
    errors = 0

    for i in range(len(productSold)):
        if productPrices[products.index(productSold[i])] != soldPrice[i]:
            errors += 1

    return errors

products = ["eggs", "milk", "cheese"]
productPrices = [2.89, 3.29, 5.79]
productSold = ["eggs", "eggs", "cheese", "milk"]
soldPrice = [2.89, 2.99, 5.97, 3.29]

errorCount = priceCheck(products, productPrices, productSold, soldPrice)
print("Number of errors:", errorCount)
