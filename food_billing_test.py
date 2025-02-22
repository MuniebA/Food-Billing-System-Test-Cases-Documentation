from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.common.action_chains import ActionChains
from webdriver_manager.chrome import ChromeDriverManager
import pandas as pd
import time
import os
from datetime import datetime


class FoodBillingTest:
    def __init__(self):
        self.driver = webdriver.Chrome(
            service=Service(ChromeDriverManager().install()))
        self.driver.maximize_window()
        # Create screenshots directory if it doesn't exist
        self.screenshots_dir = 'test_screenshots'
        os.makedirs(self.screenshots_dir, exist_ok=True)

    def take_screenshot(self, test_id, step_name):
        """
        Takes a screenshot and saves it with timestamp and test info.
        Args:
            test_id (str): The ID of the current test case
            step_name (str): Name of the test step where screenshot is taken
        """
        timestamp = datetime.now().strftime('%Y%m%d_%H%M%S')
        filename = f"{test_id}_{step_name}_{timestamp}.png"
        filepath = os.path.join(self.screenshots_dir, filename)
        try:
            self.driver.save_screenshot(filepath)
            print(f"Screenshot saved: {filepath}")
        except Exception as e:
            print(f"Failed to take screenshot: {str(e)}")

    def run_test_case(self, test_case):
        try:
            # Take screenshot before starting test
            self.take_screenshot(test_case['test_id'], 'initial_state')

            # Input quantities
            self.input_quantities(test_case)
            self.take_screenshot(test_case['test_id'], 'after_input')

            # Debug print
            print(f"Processing test {test_case['test_id']}")
            print(f"Discount value: {test_case['apply_discount']}")

            # Handle discount with explicit boolean check
            if test_case['apply_discount']:
                print(f"Applying discount for {test_case['test_id']}")
                self.apply_discount()
                self.take_screenshot(test_case['test_id'], 'after_discount')

            # Click calculate button
            calculate_button = WebDriverWait(self.driver, 10).until(
                EC.element_to_be_clickable((By.ID, "calculate"))
            )
            calculate_button.click()

            time.sleep(2)
            self.take_screenshot(test_case['test_id'], 'final_state')

            # Verify results
            if test_case['test_id'] == 'TC05':
                self.verify_error_message()
            else:
                self.verify_results(test_case)

            return True, "Test passed"

        except Exception as e:
            # Take screenshot on failure
            self.take_screenshot(test_case['test_id'], 'failure')
            return False, f"Test failed: {str(e)}"

    # Rest of the class methods remain unchanged
    def setup(self):
        self.driver.get("http://localhost/swe30009-project/index.php")
        time.sleep(2)

    def read_test_cases(self):
        df = pd.read_csv('selenium_test_cases.csv',
                         true_values=['TRUE', 'true', 'True'],
                         false_values=['FALSE', 'false', 'False'])
        print("\nCSV data after conversion:")
        print(df[['test_id', 'apply_discount']].to_string())
        return df

    def apply_discount(self):
        try:
            WebDriverWait(self.driver, 10).until(
                EC.presence_of_element_located(
                    (By.CLASS_NAME, "checkbox-wrapper"))
            )
            checkbox = self.driver.find_element(By.ID, "discount")
            self.driver.execute_script(
                "arguments[0].scrollIntoView(true);", checkbox)
            time.sleep(0.5)

            methods = [
                lambda: self.driver.execute_script(
                    """
                    arguments[0].checked = true;
                    arguments[0].dispatchEvent(new Event('change', { bubbles: true }));
                    """,
                    checkbox
                ),
                lambda: ActionChains(self.driver).move_to_element(
                    checkbox).click().perform(),
                lambda: checkbox.click()
            ]

            for method in methods:
                try:
                    method()
                    time.sleep(0.5)
                    if checkbox.is_selected():
                        print("Checkbox successfully checked")
                        break
                except:
                    continue

            if not checkbox.is_selected():
                raise Exception("Failed to select checkbox after all attempts")

        except Exception as e:
            print(f"Error applying discount: {str(e)}")
            raise e

    def input_quantities(self, test_case):
        items = {
            'Burger': 'burger_quantity',
            'Pizza': 'pizza_quantity',
            'Pasta': 'pasta_quantity',
            'Sandwich': 'sandwich_quantity',
            'Salad': 'salad_quantity',
            'Juice': 'juice_quantity',
            'Ice Cream': 'ice_cream_quantity',
            'Coffee': 'coffee_quantity'
        }

        for item_name, quantity_field in items.items():
            quantity = int(test_case[quantity_field])
            if quantity > 0:
                try:
                    item_element = WebDriverWait(self.driver, 10).until(
                        EC.presence_of_element_located((By.XPATH,
                                                        f"//h2[normalize-space()='{item_name}']/../..//input[@class='quantity']"))
                    )
                    item_element.clear()
                    item_element.send_keys(str(quantity))
                except Exception as e:
                    print(f"Error setting quantity for {item_name}: {str(e)}")

    def verify_error_message(self):
        error_message = WebDriverWait(self.driver, 10).until(
            EC.presence_of_element_located((By.CLASS_NAME, "no-items"))
        )
        assert "Please select at least one item to generate bill" in error_message.text

    def verify_results(self, test_case):
        if test_case['test_id'] == 'TC05':
            return

        bill_details = WebDriverWait(self.driver, 10).until(
            EC.presence_of_element_located((By.ID, "bill-details"))
        )

        time.sleep(1)

        total_element = WebDriverWait(self.driver, 10).until(
            EC.presence_of_element_located((By.CLASS_NAME, "bill-total"))
        )
        actual_total = float(self.get_amount_from_text(total_element.text))
        expected_total = float(test_case['expected_total'])

        assert abs(actual_total - expected_total) < 0.01, \
            f"Total mismatch. Expected: {expected_total}, Got: {actual_total}"

    def get_amount_from_text(self, text):
        amount_str = text.split('$')[1].strip().replace(',', '')
        return float(amount_str)

    def run_all_tests(self):
        test_cases = self.read_test_cases()
        results = []

        for index, test_case in test_cases.iterrows():
            print(f"\nRunning test case {test_case['test_id']}")
            success, message = self.run_test_case(test_case)
            results.append({
                'test_id': test_case['test_id'],
                'success': success,
                'message': message
            })

            self.driver.refresh()
            time.sleep(2)

        return results

    def cleanup(self):
        self.driver.quit()


def main():
    tester = FoodBillingTest()

    try:
        tester.setup()
        results = tester.run_all_tests()

        print("\nTest Results:")
        print("-------------")
        for result in results:
            status = "PASS" if result['success'] else "FAIL"
            print(f"{result['test_id']}: {status} - {result['message']}")

    finally:
        tester.cleanup()


if __name__ == "__main__":
    main()
