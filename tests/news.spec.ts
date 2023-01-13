import { test, expect } from '@playwright/test'

const testingUrl = process.env.TESTING_URL!

test.describe('homepage',() => {
  test.beforeEach(async ({ page }) => {
    await page.goto(testingUrl)
  })

  test("should have title, header and footer", async ({page}) => {
    await expect(page).toHaveTitle("Fantastic News")
    await expect(page.getByTestId("brand-name")).toHaveText("Fantastic News")
    await expect(page.getByTestId("register-link")).toBeVisible()
    await expect(page.getByTestId("login-link")).toBeVisible()
    expect(await page.getByTestId("member-username").count()).toEqual(0)
    expect(await page.getByTestId("logout-link").count()).toEqual(0)
    await expect(page.getByTestId("search")).toBeVisible()
    await expect(page.getByTestId("footer")).toBeVisible()
  })

  test("should display latest news", async ({page}) => {
    const latestArticle = page.locator('#latest-article')
    await expect(latestArticle.getByTestId("latest-article-title")).toBeVisible()
    await expect(latestArticle.getByTestId("latest-article-body")).toBeVisible()
    await expect(latestArticle.getByTestId("latest-article-date")).toBeVisible()
  })

  test("should display main news list", async ({page}) => {
    const mainArticles = page.getByTestId(/main-article-\d/)
    await expect(mainArticles).toHaveCount(4)
    for (const article of await mainArticles.all()) {
      await expect(article.getByRole("img")).toBeVisible()
      await expect(article.getByRole("heading")).toBeVisible()
    }
    const navigation = page.getByTestId("main-article-navigation")
    await expect(navigation).toBeVisible()
    await expect(navigation.getByTestId("prev-link")).toHaveClass(/disabled/)
    await expect(navigation.getByTestId("next-link")).not.toHaveClass(/disabled/)
    await expect(navigation.locator("li.active a")).toHaveText("1")
  })

  test("should display secondary news list", async ({page}) => {
    const secondaryArticles = page.getByTestId(/secondary-article-\d/)
    await expect(secondaryArticles).toHaveCount(5)
    for (const article of await secondaryArticles.all()) {
      expect(await article.getByRole("img").count()).toEqual(0)
      await expect(article.getByRole("heading")).toBeVisible()
    }
  })
})

test.describe("News Detail", () => {
  test.beforeEach(async ({ page }) => {
    await page.goto(testingUrl)
    await page.locator('#latest-article').click()
  })

  test("should render the article", async ({page}) => {
    await expect(page.getByTestId("article-title")).toBeVisible()
    await expect(page.getByTestId("article-image")).toBeVisible()
    await expect(page.getByTestId("article-body")).toBeVisible()
  })

  test.describe("Comment Section", () => {
    test("should render the comment section", async ({page}) => {
      await expect(page.getByTestId("comment-title")).toBeVisible()
      await expect(page.getByTestId("comment-list")).toBeVisible()
    })

    test("should hide the comment form if not authenticated", async ({page}) => {
      await expect(page.getByTestId("login-hint")).toBeVisible()
      expect(await page.getByTestId("comment-form").count()).toEqual(0)
    })
  })
})