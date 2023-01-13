import { test, expect, Page } from '@playwright/test'

const testingUrl = process.env.TESTING_URL!
const loginUrl = testingUrl + "/login"

export async function login(page: Page) {
    await page.goto(loginUrl)
    await expect(page.getByRole("heading")).toHaveText("Login")
    await page.locator("#id_username").fill("test_user")
    await page.locator("#id_password").fill("test_password")
    await page.locator('button:text("Login")').click();
    await expect(page).toHaveURL(testingUrl)
    await expect(page.getByTestId("logout-link")).toBeVisible()
}

test.describe('Authentication',() => {

  test.describe("Login", () => {
    test.beforeEach(async ({page}) => {
        await login(page)
    })

    test("should login a user",async ({page}) => {
        expect(await page.getByTestId("register-link").count()).toEqual(0)
        expect(await page.getByTestId("login-link").count()).toEqual(0)
        
        await expect(page.getByTestId("member-username")).toBeVisible()
        await expect(page.getByTestId("member-username")).toHaveText("test_user")
    })

    test("should logout a user", async ({page}) => {
        await page.getByTestId("logout-link").click()
        
        expect(await page.getByTestId("member-username").count()).toEqual(0)
        expect(await page.getByTestId("logout-link").count()).toEqual(0)
        
        await expect(page.getByTestId("register-link")).toBeVisible()
        await expect(page.getByTestId("login-link")).toBeVisible()
    })
  })
})