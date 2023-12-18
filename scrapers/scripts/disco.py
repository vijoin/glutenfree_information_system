def scrape(browser, product):
    page = browser.new_page()

    page.goto(product.location.base_url.format(
        name=product.name,
        brand=product.product.brand,
          ))
    page.wait_for_timeout(1000)

    #locate products results
    prices = page.locator('//div[@id="gallery-layout-container"]//article//span[contains(@class, "sellingPriceWithUnitMultiplier")]/span[2]')

    #TODO Check if product_name matches with any of the found products

    #get the price for the first result
    price = (prices.all_inner_texts())[0]

    page.close()
    
    return price
