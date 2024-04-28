query_category_prelim_str = """
Determine the query category that is the best fit for the user's query at the end of this prompt. The query categories are as follows: (1): Add column (2): Delete column (3): Update values (4): Add sentiment (5): Rename column (6): Change data type (7): Delete rows (8): Translate column (9): Ordinal encoding (10): One-hot encoding (11): Key topics (12): Semantic similarity (13): Drop duplicates (14): Impute values (15): Switch columns
The following examples are labeled with "Example 1" for the first example, "Example 2" for the second example, and so on. The answers are directly below each line labeled "Example:".
If at least one category is a good fit for the user query, then select exactly one category.
If no categories are a good fit, then select no categories and return the following: []
Only respond with the category, and no other text AT ALL! Also, do not lead off the response with a . and newline character.

Example 1: Drop column 'Industry'.
Delete column

Example 2: I want to add a new column called 'Revenue'.
Add column

Example 3: Update all 100 values across all columns to 0.
Update values

Example 4: Update all TRUE values in the 'is_won' column to 1.
Update values

Example 5: Update all 0 values in the dataframe to null
Update values

Example 6: Determine the sentiment for each value in the column 'latest_customer_tweet' with the values +, - or 0.
Add sentiment

Example 7: Rename the 'opp_type' column to 'opportunity_type'.
Rename column

Example 8: Change the data type of the 'is_won' column to int
Change data type

Example 9: Change the data type of 'outbound_emails' to int
Change data type

Example 10: Change the data type of 'is_won' to bool
Change data type

Example 11: Delete row 3.
Delete rows

Example 12: Delete rows 1 and 2
Delete rows

Example 13: Translate the 'latest_customer_tweet' column from English to Spanish
Translate column

Example 14: Apply ordinal encoding to the 'Industry' column
Ordinal encoding

Example 15: Apply one-hot encoding to the 'Industry' column
One-hot encoding

Example 16: Get the key topics for 'latest_customer_tweets'
Key topics

Example 17: Calculate the semantic similarity between 'latest_customer_tweet' and 'latest_customer_tweet_old'
Semantic similarity

Example 18: Drop duplicate rows associated with the 'Industry' column
Drop duplicates

Example 19: Fill in all missing values
Impute values

Example 20: Switch the 'Industry' and 'created' column order
Switch columns

Example 21: What is your favorite Marvel superhero and why?
[]

Example 22: Why do you like the New York Yankees instead of the New York Mets?
[]

Example 23: Get the sentiment from the 'latest_customer_tweet' column
Add sentiment

The user question is as follows: """

drop_column_prelim_str = """
Write a syntactically correct pandas one-liner involving a dataframe called 'df_data' for a drop column request from the user. Below are examples of what a user request and correct answer should look like.
The answer should always have a keyword argument, 'axis=1'.
The examples are labeled with "Example 1" for the first example, "Example 2" for the second example, and so on. The answers are directly below each line labeled "Example:"
The words "Answer" and "Example" should NEVER be part of any answer, NO MATTER WHAT!

Example 1: Drop column 'Industry'.
df_data.drop(['Industry'], axis=1)

Example 2: I want to drop the 'opp_type' column.
df_data.drop(['opp_type'], axis=1)

Example 3: I want to drop the 'opp_type', 'Industry' and 'opportunity_name' columns.
df_data.drop(['opp_type', 'Industry', 'opportunity_name'], axis=1)

The user request is as follows:
"""

add_column_prelim_str = """
Write a syntactically correct pandas one-liner involving a dataframe called 'df_data' for an add column request from the user. Below are examples of what a user request and correct answer should look like.
The new column should not contain any non-empty values. 
The examples are labeled with "Example 1" for the first example, "Example 2" for the second example, and so on. The answers are directly below each line labeled "Example:"
The words "Answer" and "Example" should NEVER be part of any answer, NO MATTER WHAT!

Example 1: Add a new column called 'Sentiment'.
df_data.assign(Sentiment=None)

Example 2: I want to add a new column called 'Revenue'.
df_data.assign(Revenue=None)

Example 3: Add column 'Description'.
df_data.assign(Description=None)
"""

update_values_prelim_str = """
Write a syntactically correct pandas one-liner involving a dataframe called 'df_data' for an update values request from the user. Below are examples of what a user request and correct answer should look like.
The examples are labeled with "Example 1" for the first example, "Example 2" for the second example, and so on. The answers are directly below each line labeled "Example:"
The words "Answer" and "Example" should NEVER be part of any answer, NO MATTER WHAT!

Example 1: Update all values that are null to a new value of 0.
df_data.replace(np.nan, 1)

Example 2: Replace all values for all columns that are 3 to 5.
df_data.replace(3, 5)

Example 3: Change all 100 values across all columns to 0.
df_data.replace(100, 0)

Example 4: Change all 0 values under the 'meetings' column to null.
df_data.replace(to_replace=0, value={'meetings':np.nan })

Example 5: Change all 'TRUE' values under the 'is_closed' column to 'True'
df_data.replace(to_replace='TRUE', value={'is_closed':'True' })

Example 6: Change all 0 values under the 'meetings' column and 'calls' column to null
df_data.replace(to_replace=0, value={'meetings':np.nan, 'calls':np.nan })
"""

rename_column_prelim_str = """
Write a syntactically correct pandas one-liner involving a dataframe called 'df_data' for an add column request from the user. Below are examples of what a user request and correct answer should look like.
The new column should not contain any non-empty values. 
The examples are labeled with "Example 1" for the first example, "Example 2" for the second example, and so on. The answers are directly below each line labeled "Example:"
The words "Answer" and "Example" should NEVER be part of any answer, NO MATTER WHAT!

Example 1: Rename the 'created' column to 'created_date'
df_data.rename(columns={'created': 'created_date'})

Example 2: Change the name of the 'opportunity_id' column to 'opp_id'
df_data.rename(columns={'opportunity_id': 'opp_id'})

Example 3: Change the names of the 'opportunity_id' and 'expected_close_date' columns to 'opp_id' and 'close_date', respectively
df_data.rename(columns={'opportunity_id': 'opp_id', 'expected_close_date': 'close_date'})

Example 4: Change the names of the 'opportunity_id' and 'opportunity_name' columns to 'opp_id' and 'opp_name'
df_data.rename(columns={'opportunity_id': 'opp_id', 'opportunity_name': 'opp_name'})
"""

change_data_type_prelim_str = """
Write a syntactically correct pandas one-liner involving a dataframe called 'df_data' for a change column data type request from the user. Below are examples of what a user request and correct answer should look like.
The examples are labeled with "Example 1" for the first example, "Example 2" for the second example, and so on. The answers are directly below each line labeled "Example:"
The words "Answer" and "Example" should NEVER be part of any answer, NO MATTER WHAT!

Example 1: Change the data type of the 'pushed_out' column to float
df_data.assign(pushed_out=df_data['pushed_out'].astype('float'))

Example 2: Change the data type of the 'is_won' column to int
df_data.assign(is_won=df_data['is_won'].astype('int'))

Example 3: Change the data type of the 'is_won' column to boolean
df_data.assign(is_won=df_data['is_won'].astype('bool'))

Example 4: Change the data types of the 'is_won' and 'pushed_out' columns to boolean and float
df_data.assign(is_won=df_data['is_won'].astype('bool'),pushed_out=df_data['pushed_out'].astype('float'))
"""

delete_rows_prelim_str = """
Write a syntactically correct pandas one-liner involving a dataframe called 'df_data' for a delete row request from the user. Below are examples of what a user request and correct answer should look like.
The new column should not contain any non-empty values. 
The examples are labeled with "Example 1" for the first example, "Example 2" for the second example, and so on. The answers are directly below each line labeled 'Example':
The words 'Answer' and 'Example' should NEVER be part of any answer, NO MATTER WHAT!

Example 1: Delete row 3
df_data.drop([3])

Example 2: Delete row 1
df_data.drop([1])

Example 3: Delete rows 1 and 2
df_data.drop([1,2])

Example 4: Delete rows 1 through 3
df_data.drop([1,2,3])
"""

switch_columns_prelim_str = """
Write a syntactically correct pandas one-liner involving a dataframe called 'df_data' for a switch columns request from the user. Below are examples of what a user request and correct answer should look like.
The new column should not contain any non-empty values. 
The examples are labeled with "Example 1" for the first example, "Example 2" for the second example, and so on. The answers are directly below each line labeled 'Example':
The words 'Answer' and 'Example' should NEVER be part of any answer, NO MATTER WHAT!

Example 1: Switch the 'Industry' and 'created' column order
df_data.assign(**df_data.iloc[:, [df_data.columns.get_loc('created'), df_data.columns.get_loc('Industry')] + list(range(len(df_data.columns)))[df_data.columns.get_loc('created')+1:] + list(range(len(df_data.columns)))[:df_data.columns.get_loc('created')]].to_dict(orient='series'))

Example 2: Switch 'Industry' and 'created'
df_data.assign(**df_data.iloc[:, [df_data.columns.get_loc('created'), df_data.columns.get_loc('Industry')] + list(range(len(df_data.columns)))[df_data.columns.get_loc('created')+1:] + list(range(len(df_data.columns)))[:df_data.columns.get_loc('created')]].to_dict(orient='series'))

Example 3: Switch the 'Industry' column with the 'created' column
df_data.assign(**df_data.iloc[:, [df_data.columns.get_loc('created'), df_data.columns.get_loc('Industry')] + list(range(len(df_data.columns)))[df_data.columns.get_loc('created')+1:] + list(range(len(df_data.columns)))[:df_data.columns.get_loc('created')]].to_dict(orient='series'))
"""

drop_duplicates_prelim_str = """
Write a syntactically correct pandas one-liner involving a dataframe called 'df_data' for a drop duplicates from the user. Below are examples of what a user request and correct answer should look like.
The new column should not contain any non-empty values. 
The examples are labeled with "Example 1" for the first example, "Example 2" for the second example, and so on. The answers are directly below each line labeled 'Example':
The words 'Answer' and 'Example' should NEVER be part of any answer, NO MATTER WHAT!

Example 1: Drop duplicate rows associated with the 'Industry' column
df_data.drop_duplicates(subset='Industry')

Example 2: Drop dups associated with the 'Industry' column
df_data.drop_duplicates(subset='Industry')

Example 3: Drop duplicate rows using 'Industry'
df_data.drop_duplicates(subset='Industry')

Example 4: Drop dups from 'Industry'
df_data.drop_duplicates(subset='Industry')
"""

impute_values_prelim_str = """
Write a syntactically correct pandas one-liner involving a dataframe called 'df_data' for a impute values from the user. Below are examples of what a user request and correct answer should look like.
The new column should not contain any non-empty values. 
The examples are labeled with "Example 1" for the first example, "Example 2" for the second example, and so on. The answers are directly below each line labeled 'Example':
The words 'Answer' and 'Example' should NEVER be part of any answer, NO MATTER WHAT!

Example 1: Impute all blank values based on the data type of the column
df_data.fillna(value=imputation_values)

Example 2: Fill in all missing values based on the data type of the column
df_data.fillna(value=imputation_values)

Example 3: Fill in all missing values
df_data.fillna(value=imputation_values)
"""

one_hot_encoding_prelim_str = """
Write a syntactically correct pandas one-liner involving a dataframe called 'df_data' for a one-hot encoding request from the user. Below are examples of what a user request and correct answer should look like.
The new column should not contain any non-empty values. 
The examples are labeled with "Example 1" for the first example, "Example 2" for the second example, and so on. The answers are directly below each line labeled 'Example':
The words 'Answer' and 'Example' should NEVER be part of any answer, NO MATTER WHAT!

Example 1: Apply one-hot encoding to the 'Industry' column
pd.get_dummies(df_data, columns=['Industry'])

Example 2: Apply OHE to the 'Industry' column
pd.get_dummies(df_data, columns=['Industry'])

Example 3: One-hot encode the 'Industry' column
pd.get_dummies(df_data, columns=['Industry'])
"""

ordinal_encoding_prelim_str = """
Write a syntactically correct pandas one-liner involving a dataframe called 'df_data' for an ordinal encoding request from the user. Below are examples of what a user request and correct answer should look like.
The new column should not contain any non-empty values. 
The examples are labeled with "Example 1" for the first example, "Example 2" for the second example, and so on. The answers are directly below each line labeled 'Example':
The words 'Answer' and 'Example' should NEVER be part of any answer, NO MATTER WHAT!

Example 1: Apply ordinal encoding to the 'Industry' column
df_data.assign(Industry=df_data['Industry'].astype('category').cat.codes)

Example 2: I want the 'Industry' column to have ordinal encoding
df_data.assign(Industry=df_data['Industry'].astype('category').cat.codes)

Example 3: Provide ordinal encoding to the 'Industry' column
df_data.assign(Industry=df_data['Industry'].astype('category').cat.codes)
"""

add_sentiment_column_prelim_str = """
Write a syntactically correct pandas one-liner involving a dataframe called 'df_data' for an add sentiment column request from the user. Below are examples of what a user request and correct answer should look like.
The examples are labeled with "Example 1" for the first example, "Example 2" for the second example, and so on. The answers are directly below each line labeled "Example:"
The words "Answer" and "Example" should NEVER be part of any answer, NO MATTER WHAT!

Example 1: Determine the sentiment for each value in the 'latest_customer_tweet' column by assigning a +, - or 0.
df_data.assign(sentiment=df_data['latest_customer_tweet'].apply(lambda x: '+' if TextBlob(x).sentiment.polarity > 0 else ('-' if TextBlob(x).sentiment.polarity < 0 else '0')))

Example 2: Determine the sentiment for each value in the column 'latest_customer_tweet' with the values +, - or 0.
df_data.assign(sentiment=df_data['latest_customer_tweet'].apply(lambda x: '+' if TextBlob(x).sentiment.polarity > 0 else ('-' if TextBlob(x).sentiment.polarity < 0 else '0')))

Example 3: Include a 'sentiment' column that contains values (+, -, 0) associated with each row in the 'latest_customer_tweet' column
df_data.assign(sentiment=df_data['latest_customer_tweet'].apply(lambda x: '+' if TextBlob(x).sentiment.polarity > 0 else ('-' if TextBlob(x).sentiment.polarity < 0 else '0')))

Example 4: Get the sentiment from the 'latest_customer_tweet' column
df_data.assign(sentiment=df_data['latest_customer_tweet'].apply(lambda x: '+' if TextBlob(x).sentiment.polarity > 0 else ('-' if TextBlob(x).sentiment.polarity < 0 else '0')))
"""

key_topic_words_prelim_str = """
Write a syntactically correct pandas one-liner involving a dataframe called 'df_data' for a key topics request from the user. Below are examples of what a user request and correct answer should look like.
The examples are labeled with "Example 1" for the first example, "Example 2" for the second example, and so on. The answers are directly below each line labeled "Example:"
The words "Answer" and "Example" should NEVER be part of any answer, NO MATTER WHAT!

Example 1: Get the key topics for each row of the 'latest_customer_tweets' column
df_data.assign(key_topic_words=df_data['latest_customer_tweet'].apply(lambda x: [word for word, pos in pos_tag(word_tokenize(x)) if pos.startswith('N')]))

Example 2: Get the key topics for 'latest_customer_tweets'
df_data.assign(key_topic_words=df_data['latest_customer_tweet'].apply(lambda x: [word for word, pos in pos_tag(word_tokenize(x)) if pos.startswith('N')]))

Example 3: Get the topics for the 'latest_customer_tweets' column
df_data.assign(key_topic_words=df_data['latest_customer_tweet'].apply(lambda x: [word for word, pos in pos_tag(word_tokenize(x)) if pos.startswith('N')]))
"""

semantic_similarity_prelim_str = """
Write a syntactically correct pandas one-liner involving a dataframe called 'df_data' for a semantic similarity request from the user. Below are examples of what a user request and correct answer should look like.
The examples are labeled with "Example 1" for the first example, "Example 2" for the second example, and so on. The answers are directly below each line labeled "Example:"
The words "Answer" and "Example" should NEVER be part of any answer, NO MATTER WHAT!

Example 1: Get the semantic similarity between the 'latest_customer_tweet' and 'latest_customer_tweet_old' columns
df_data.assign(similarity=df_data.apply(calculate_similarity, axis=1))

Example 2: Calculate the semantic similarity between 'latest_customer_tweet' and 'latest_customer_tweet_old'
df_data.assign(similarity=df_data.apply(calculate_similarity, axis=1))

Example 3: Calculate the semantic similarity value between 'latest_customer_tweet' and 'latest_customer_tweet_old'
df_data.assign(similarity=df_data.apply(calculate_similarity, axis=1))
"""

translate_text_column_prelim_str = """
Write a syntactically correct pandas one-liner involving a dataframe called 'df_data' for a text column translation request from the user. Below are examples of what a user request and correct answer should look like.
The examples are labeled with "Example 1" for the first example, "Example 2" for the second example, and so on. The answers are directly below each line labeled "Example:"
The words "Answer" and "Example" should NEVER be part of any answer, NO MATTER WHAT!

Example 1: Translate the 'latest_customer_tweet' column from English to Spanish
df_data.assign(latest_customer_tweet=df_data['latest_customer_tweet'].apply(translator.translate, src='en', dest='es').apply(getattr, args=('text',)))

Example 2: Translate the 'latest_customer_tweet' column from Spanish to English
df_data.assign(latest_customer_tweet=df_data['latest_customer_tweet'].apply(translator.translate, src='es', dest='en').apply(getattr, args=('text',)))

Example 3: Translate the 'latest_customer_tweet' column from English to French
df_data.assign(latest_customer_tweet=df_data['latest_customer_tweet'].apply(translator.translate, src='en', dest='fr').apply(getattr, args=('text',)))
"""