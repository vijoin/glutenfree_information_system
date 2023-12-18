def scrape(browser, product):
    page = browser.new_page()

    page.goto(product.location.base_url.format(
        name=product.name,
        brand=product.product.brand,
          ).replace(' ', '+'))
    page.wait_for_timeout(1000)

    #locate products results
    prices = page.locator('//div[@id="catalogoProductos"]//div[@class="precios"]//span[@class="monto"]')

    #Check if product_name matches with the any of the found products

    #get the price for the first result
    price = (prices.all_inner_texts())[0]

    page.close()

    return price