from selenium import webdriver
from selenium.common import ElementNotInteractableException, TimeoutException, NoSuchElementException
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.by import By
from selenium.webdriver.support.wait import WebDriverWait
from selenium.webdriver.support import expected_conditions as ec

import Serializer
from Offer import Offer

def modified_offers(offers_set: set[Offer], previous_offers: set[Offer]) -> set[Offer]:
    updated: set[Offer] = set()
    common_offers = offers_set.intersection(previous_offers)
    for offer in common_offers:
        # Find the corresponding offer in the previous set to compare the date
        previous_offer = [p_offer for p_offer in previous_offers if p_offer == offer][0]
        new_offer = [p_offer for p_offer in offers_set if p_offer == offer][0]
        if new_offer.date != previous_offer.date:
            updated.add(offer)
    return updated

if __name__ == "__main__":
    options = Options()
    options.add_argument('--headless')  # Run in headless mode
    driver = webdriver.Chrome(options=options)

    # Navigate to the URL
    driver.get('https://www.olx.pl/nieruchomosci/mieszkania/sprzedaz/wroclaw/?search%5Border%5D=created_at:desc&search%5Bfilter_enum_builttype%5D%5B0%5D=blok&search%5Bfilter_enum_market%5D%5B0%5D=primary')

    # accept cookies
    cookie_button = WebDriverWait(driver, 3).until(
        ec.element_to_be_clickable((By.ID, "onetrust-accept-btn-handler"))
    )
    cookie_button.click()

    page: int = 1
    offers_set: set[Offer] = set()

    print("Scanning offers...")

    # go through pages and get offers
    while True:
        print(f"page: {page}")
        offers = driver.find_elements(By.XPATH, '//div[@data-cy="l-card"]')
        for offer in offers:
            offer_id = offer.get_attribute('id')
            ref = offer.find_element(By.XPATH, './div/div/div[2]/div/a').get_attribute('href')
            title = offer.find_element(By.XPATH, './div/div/div[2]/div/a/h4').text
            price = offer.find_element(By.XPATH, './div/div/div[2]/div/p').text
            location_date = offer.find_element(By.XPATH, './div/div/div[2]/div[3]/p').text
            # print(f"location-date: {location_date}")
            location = location_date.split("-")[0].strip()
            date = location_date.split("-")[1].strip().lower()
            offers_set.add(Offer(offer_id, title, price, location, date, ref))
            # print(f"oferta: {title}")
            # print(f"cena: {price}")
            # print(f"lokacja: {location}")
            # print(f"data: {date}")
            # print(f"id {offer_id}")
            # print(f"link: {ref}")
            # print()

        try:
            # next page
            WebDriverWait(driver, 5).until(
                ec.element_to_be_clickable((By.XPATH, '//a[@data-cy="pagination-forward"]'))
            )
            next_page = driver.find_element(By.XPATH, '//a[@data-cy="pagination-forward"]')
            next_page.click()
            WebDriverWait(driver, 5).until(
                ec.presence_of_element_located((By.XPATH, '//div[@data-cy="l-card"]'))
            )
            page+= 1
        except (ElementNotInteractableException, TimeoutException, NoSuchElementException) as e:
            driver.quit()
            break


    # offers comparison
    previous_offers = Serializer.load_offers()
    new_offers: set[Offer] = offers_set - previous_offers
    deleted_offers: set[Offer] = previous_offers - offers_set
    updated_offers: set[Offer] = modified_offers(offers_set, previous_offers)

    print(f"new offers: {len(new_offers)}")
    print(new_offers)
    print("-----------------")
    print(f"deleted offers: {len(deleted_offers)}")
    print(deleted_offers)
    print("-----------------")
    print(f"updated offers: {len(updated_offers)}")
    print(updated_offers)
    print("\n\n")

    # Save the current offers to a file
    Serializer.save_offers(offers_set)




