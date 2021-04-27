# Hello Fresh - Recipes ETL

## Compliments
1) The challenge is fun to code.
2) It's clear about the needs.
3) It covers a good part of what is demanded from a data engineer.
4) It's business related.

##Approach
After reading the challenge, it was clear that the two tasks would become two jobs. The first one for ingestion and the 
second with the analysis. For the first task the most important part was Data exploration.

##Data exploration
### Cook Time & Prep Time
After looking at the recipes, the first problem I found was the prepTime & cookTime, the string format was hard to solve 
because it was not default, not even string default. The easiest way of solving it was with a user defined function. Knowing more about this fields
I think it will be possible to solve the problem using just spark functions, but at this point I found the udf more flexible.
In the UDF I assumed that the format will always be `PT99H99M` when present.

### Ingredients
That was the field I was more concerned of.
At first, I thought about putting it on a map, where the keys would be the
ingredients and the values the amount, then I thought about having an extra table just for ingredients and the recipes, which would be great for categorizing ingredients like (vegan, dairy free, gluten free, etc...) and add a lot of flexibility on
recipes search engines. The problem was that, the ingredients are not homogeneous. You can have:
* 1 pinch of salt
* pepper to taste
* 1 cup / 250ml milk
* 2 slices of bread

So I'd have to spend a lot of time parsing it. For this test, I kept it as string and filtered by the string 'beef'. Which is
not the best solution I would create for a production application.

### Published Date and Recipe Yield
Those two fields were pretty straight forward, just a simple cast that add a lot of possibilities.
In case of publishedDate can be used for partitions and the recipeYield can be used for example when you are looking for a recipe for 6+ people.

### Data filtering
I didn't filter any data when processing the ingestion, I found that everything could be used and generating the final CSV would work with the data provided.


## Bonus
* Config management: I tried to keep the spark submit job as simple as possible, it's still able to adjust spark parameters.
* Logging and alerting: I actually didn't use much of those, I found the spark job log already too verbose, sometimes it's hard to find what you're looking for. I try to keep simple messages in general and add more detailed logs to specific parts of the code that tent to be problematic.
* Data quality checks: Just verified if the source dataframe has records, if it doesn't raises exception.
* CI/CD / Scheduling: I would combine CircleCi or Jenkins with Apache Airflow, this part id very versatile now that there are CI tools on Github and AWS.
* Performance: Well, as I mentioned before, the UDF and the 'Ingredients' field can be problematic. Replacing the UDF with spark native would be great. About
the ingredients field, preprocessing it in order to have something more organized can also help on future searches. There are many other factors that can impact performance, like partitions, file sizing, json files instead of avro files etc... we can also talk about them. 
* Software & Data Engineering: I tried to keep the code organized and decoupled. I didn't find much room for complex classes / extensions/ inheritance, but that's a subject that I enjoy a lot, and I'm happy that you are concened about it.
  

### PS. Exception Handling
On the readme you mentioned the need for proper exception handling. I found it difficult to find a situation where
exceptions should be treated in this scenario: different formats? empty datasets? missing columns?
For all of those that I was thinking of, I would not try to treat the exception. All of them should be critical alerts.
I spent less time than I wanted on this, so maybe we could talk about that on the next steps.


```
Thank you for the opportunity and I'm sorry for the delay.
Henrique.
```


