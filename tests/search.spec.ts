import { test, expect, Page } from '@playwright/test'

const testingUrl = process.env.TESTING_URL!

test.describe("Article Search", () => {
    test.beforeEach(async ({ page }) => {
      await page.goto(testingUrl)
    })

    test("should show search results if articles found",async ({page}) => {
      // Fill search form and submit
      await page.getByTestId("search").locator("input").fill("Test")
      await page.getByTestId("search").locator("button").click()
      // Expect search results to load with 10 results
      await expect(page).toHaveURL(testingUrl + "/search-results/?keywords=Test")
      await expect(page.locator(".card")).toHaveCount(10)
      // Expect pagination controls to be displayed correctly
      const navigation = page.getByTestId("article-navigation")
      await expect(navigation).toBeVisible()
      await expect(navigation.getByTestId("prev-link")).toHaveCount(0)
      await expect(navigation.getByTestId("next-link")).not.toHaveClass(/disabled/)
      await expect(navigation.locator("li.active a")).toHaveText("1")
    })

    
    test("should show empty result if no article was found",async ({page}) => {
      await page.getByTestId("search").locator("input").fill("ImpossibleToFind")
      await page.getByTestId("search").locator("button").click()
      await expect(page).toHaveURL(testingUrl + "/search-results/?keywords=ImpossibleToFind")
      await expect(page.locator(".card")).toHaveCount(0)
      await expect(page.locator("p", {hasText: "No article found."})).toBeVisible()
    })
})

