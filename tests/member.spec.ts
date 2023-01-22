import { test, expect, Page } from '@playwright/test'

const testingUrl = process.env.TESTING_URL!
const loginUrl = testingUrl + "/login"
const registerUrl = testingUrl + "/register"

export async function login(page: Page, username="test_user") {
    await page.goto(loginUrl)
    await page.locator("#id_username").fill(username)
    await page.locator("#id_password").fill("test_password")
    await page.locator('button:text("Login")').click();
}

test.describe('Authentication',() => {

  test.describe("Login", () => {

    test("should login a user",async ({page}) => {
        await login(page)
        await expect(page.getByTestId("register-link")).toHaveCount(0)
        await expect(page.getByTestId("login-link")).toHaveCount(0)
        
        await expect(page).toHaveURL(testingUrl)
        await expect(page.getByTestId("logout-link")).toBeVisible()
        
        await expect(page.getByTestId("member-username")).toBeVisible()
        await expect(page.getByTestId("member-username")).toHaveText("test_user")
    })

    test("should not login an invalid user",async ({page}) => {
        await login(page, "invalid_user")
        
        await expect(page).toHaveURL(loginUrl)
        await expect(page.locator("form .alert")).toBeVisible()
    })

    test("should logout a user", async ({page}) => {
        await login(page)
        await page.getByTestId("logout-link").click()
        
        await expect(page.getByTestId("member-username")).toHaveCount(0)
        await expect(page.getByTestId("logout-link")).toHaveCount(0)
        
        await expect(page.getByTestId("register-link")).toBeVisible()
        await expect(page.getByTestId("login-link")).toBeVisible()
    })
  })

  test.describe("Login", () => {

    test.beforeEach(async ({page}) => {
      await page.goto(registerUrl)
    })

    test("should register a user",async ({page}) => {
      const username = "test_user" + new Date().getTime()
      await page.locator("#id_username").fill(username)
      await page.locator("#id_first_name").fill("test_user")
      await page.locator("#id_email").fill("test_user@test.com")
      await page.locator("#id_password1").fill("test_password")
      await page.locator("#id_password2").fill("test_password")
      await page.locator('form button:text("Register")').click();
      await expect(page).toHaveURL(testingUrl)
      await expect(page.getByTestId("logout-link")).toBeVisible()
      await expect(page.getByTestId("member-username")).toBeVisible()
      await expect(page.getByTestId("member-username")).toHaveText(username)
    })

    test("should show error if data is invalid",async ({page}) => {
      const username = "test_user"
      await page.locator("#id_username").fill(username)
      await page.locator("#id_first_name").fill("test_user")
      await page.locator("#id_email").fill("test_user@test.com")
      await page.locator("#id_password1").fill("test_password1")
      await page.locator("#id_password2").fill("test_password2")
      await page.locator('form button:text("Register")').click();
      await expect(page).toHaveURL(registerUrl)
      await expect(page.locator("#error_1_id_username")).toBeVisible()
      await expect(page.locator("#error_1_id_password2")).toBeVisible()
    })
  })
})