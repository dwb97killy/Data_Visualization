import pandas
import matplotlib.pyplot as plt
from datetime import datetime
from pytz import utc

data = pandas.read_csv("reviews.csv", parse_dates=["Timestamp"])
data.head()

data["Day"] = data["Timestamp"].dt.date

day_count = data.groupby(["Day"]).count()
plt.figure(figsize=(25, 3))
plt.plot(day_count .index, day_count["Comment"])

day_average = data.groupby(["Day"]).mean()
print(day_average)
print(type(day_average))
print(type(data))
plt.figure(figsize=(25, 3))
plt.plot(day_average.index, day_average["Rating"])


# Downsampling by week
data["Week"] = data["Timestamp"].dt.strftime("%Y-%U")
# data.head()
week_average = data.groupby(["Week"]).mean()
plt.figure(figsize=(25, 3))
plt.plot(week_average.index, week_average["Rating"])


# Downsampling by month
data["Month"] = data["Timestamp"].dt.strftime("%Y-%m")
# data.head()
month_average = data.groupby(["Month"]).mean()
print(month_average.loc["2018-01"])
plt.figure(figsize=(25, 3))
plt.plot(month_average.index, month_average["Rating"])


# Average by month and course
month_course_average = data.groupby(["Month", "Course Name"]).mean().unstack()
# print(month_course_average)
# print(month_course_average.index)
# print(month_course_average.columns)
# print(data.index)
# print(data.columns)
month_course_average.plot(figsize=(25, 10))

month_course_comment = data.groupby(["Month", "Course Name"])["Comment"].count().unstack()
month_course_comment.plot(figsize=(25, 10))


# The happiest day
data["Weekday"] = data["Timestamp"].dt.strftime("%A")
data["Day Number"] = data["Timestamp"].dt.strftime("%w")
weekday_average = data.groupby(["Weekday", "Day Number"]).mean()
weekday_average = weekday_average.sort_values("Day Number")
plt.figure()
plt.plot(weekday_average.index.get_level_values(0), weekday_average["Rating"])


# Rating and comments for different courses
course_comment = data.groupby(["Course Name"])["Comment"].count()
# print(course_comment)
plt.figure()
plt.pie(course_comment, labels=course_comment.index)

course_rating = data.groupby(["Course Name"])["Rating"].count()
plt.figure()
plt.pie(course_rating, labels=course_rating.index)


# The comment-to-rating ratio for different courses
course_ratio = pandas.merge(course_comment, course_rating, on="Course Name")
course_ratio["Ratio"] = (course_ratio["Comment"] / course_ratio["Rating"])
# print(course_ratio)
plt.figure(figsize=(25, 3))
plt.plot(course_ratio.index, course_ratio["Ratio"])

plt.show()

