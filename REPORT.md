# Final Report: TMDB Movie Data Analysis

**Author:** Dushimimana Prince
**Programme:** AmaliTech Data Engineering Apprenticeship

---

## 1. Objective

Build a pipeline that fetches movie data from the TMDB API, cleans it, and answers four questions:

1. Which movies perform best and worst, financially and with audiences?
2. Can the data answer targeted search queries?
3. Do franchise movies perform better than standalone movies?
4. Which franchises and directors are the most successful?

---

## 2. Methodology

**Data.** 24 movies: the 18 valid IDs from the brief (ID `0` does not exist and tests error handling) plus 6 movies added so the two required searches return results.

**Extraction.** One request per movie to `/movie/{id}?append_to_response=credits`, which returns details and cast/crew together. Each request has a 10-second timeout and up to 3 retries. Missing movies (404) are skipped and an invalid key (401) stops the run. Raw data is saved locally so the analysis is repeatable.

**Cleaning.** Unused columns were dropped and nested JSON was flattened into text. Data types were fixed, and unrealistic zeros and placeholder text were replaced with `NaN`. Budget and revenue were then converted to millions of USD; this happens after the zeros are replaced, so an unknown budget can never become `0.0` and distort ROI. Duplicates, incomplete rows and unreleased movies were removed, and the columns were put in the required order. A validation step confirmed every rule.

**Analysis.**
- **Exploratory analysis:** missing values, summary statistics and outliers (IQR rule).
- **KPI rankings:** 10 rankings through one reusable function, with a $10M budget minimum for ROI and a 10-vote minimum for ratings.
- **Comparisons:** two search queries, a franchise vs. standalone comparison, and top franchise and director rankings.
- **Charts:** five, made with Matplotlib.

---

## 3. Key insights

**1. Every movie in the sample was profitable.**
All 24 movies earned more than their budget. Avatar had both the highest profit ($2,687M) and the highest ROI (12.3×). Even the weakest performer, Looper, returned 1.6× its budget. The "lowest" rankings therefore show the weakest of very successful films, not flops.

**2. Franchises earn more and return more per dollar, but are not rated higher.**

| | Movies | Mean revenue | Median ROI | Mean budget | Mean popularity | Mean rating |
|---|---|---|---|---|---|---|
| Franchise | 18 | $1,522M | 7.31× | $197M | 36.5 | 7.45 |
| Standalone | 6 | $768M | 5.93× | $105M | 27.0 | 7.45 |

Franchise movies cost almost twice as much but earn about twice as much, with a better median ROI and higher popularity. Both groups have exactly the same mean rating: the commercial advantage of franchises does not come from audiences liking them more.

**3. Popularity and rating are strongly linked.**
The correlation is 0.73: better-rated movies tend to be more popular. The main exception is Pulp Fiction, the highest-rated movie (8.48) but only moderately popular, because TMDB popularity reflects current activity and older films attract less of it.

**4. A few franchises and directors dominate revenue.**
The Avengers Collection is the most successful franchise in the sample (4 movies). James Cameron leads the directors ($5,188M from 2 movies). Joe and Anthony Russo follow ($4,991M) with the highest mean rating (8.25), so in this sample the top-earning directors are also among the best rated.

**5. Genre results need care.**
Romance, Fantasy and Drama show the highest median ROI, and Crime and Action the lowest. However, the top genres rest on only a few movies each, so one title such as Titanic can decide their result.

---

## 4. Limitations

- **Selection bias:** the sample is 24 hand-picked, mostly record-breaking movies, so the results describe the top of the box office, not movies in general.
- **Small groups:** the standalone group (6 movies) and several genres contain very few movies.
- **No inflation adjustment:** money values are in nominal dollars, which favours recent movies in year-on-year comparisons.
- **Source data:** TMDB budgets and revenues are maintained by its community and may differ from official studio figures.

---

## 5. Conclusions

Franchise blockbusters dominate box office revenue and also return more per dollar, while audiences rate them no higher than standalone films. Popularity and rating move together, with older classics as the main exception.

The pipeline is modular and repeatable: extraction, cleaning, analysis and charts each live in their own module, and the whole analysis reruns from the notebook with one command. To make the conclusions apply more widely, the next step would be to fetch a larger, random sample of released movies through TMDB's `/discover/movie` endpoint and adjust financial figures for inflation.