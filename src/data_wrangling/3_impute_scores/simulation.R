# cleanup
rm(list=ls()); gc(); cat("\014"); try(dev.off(), silent=T)

# libraries
library(tidyverse)

#---- ics-level data ----#

# number of departments
ndept <- 200

# maximum number of case studies for a department
maxcase <- 7

# number of case studies per department
ncase <- sample(6:maxcase, size=ndept, replace=TRUE)

# ics-level data frame
dat_ics <- data.frame(
    dept = rep(1:ndept, ncase),
    case = unlist(lapply(ncase, function(x) seq(1:x)))
)

# generate covariate (in this case one-dimensional)
set.seed(1704)
dat_ics$x1 <- as.numeric(runif(nrow(dat_ics), 1, 4))
dat_ics$x2 <- dat_ics$x1^3
dat_ics$x3 <- dat_ics$x1^(1/3)

# generate stars for various functional form complexities
## Function to map outcome to 4 star levels
#' @param y_num numeric outcome
#' @return outcome in four levels
shrink_to_stars <- function(y_num) {
    y_star <- case_when(
        y_num <= quantile(y_num)[[2]] ~ 1,
        y_num <= quantile(y_num)[[3]] ~ 2,
        y_num <= quantile(y_num)[[4]] ~ 3,
        y_num > quantile(y_num)[[4]] ~ 4
    )
    
    assertthat::assert_that(max(y_star) <= 4)
    assertthat::assert_that(min(y_star) >= 1)
    return(y_star)
}

y_sd <- 0.25
dat_ics$y1 <- shrink_to_stars(rnorm(nrow(dat_ics), 0, y_sd) + dat_ics$x1)
dat_ics$y2 <- shrink_to_stars(rnorm(nrow(dat_ics), 0, y_sd) + dat_ics$x2)
dat_ics$y3 <- shrink_to_stars(rnorm(nrow(dat_ics), 0, y_sd) + dat_ics$x3)

plot(dat_ics$x1, dat_ics$y1)
plot(dat_ics$x2, dat_ics$y2)
plot(dat_ics$x3, dat_ics$y3)

## Train and test data
dat_ics$id <- 1:nrow(dat_ics)
set.seed(1704)
dat_ics_train <- sample_frac(dat_ics, 0.8)
dat_ics_test <- dat_ics[!(dat_ics$id %in% dat_ics_train$id), ]

dat_dept_train <- dat_ics_train %>%
    select(-id, -case) %>%
    group_by(dept) %>%
    summarise(
        y1 = mean(y1),
        y2 = mean(y2),
        y3 = mean(y3),
        x1 = mean(x1),
        x2 = mean(x2),
        x3 = mean(x3)
    )

## Model performance
## Linear relationship
ics_model1 <- lm(y1 ~ x1, data = dat_ics_train)
mean(round(predict(ics_model1, dat_ics_test)) == dat_ics_test$y1) ## 0.74
dept_model1 <- lm(y1 ~ x1, data = dat_dept_train)
mean(round(predict(dept_model1, dat_ics_test)) == dat_ics_test$y1) ## 0.75

## Quadratic relationship
ics_model2 <- lm(y2 ~ x2, data = dat_ics_train)
mean(round(predict(ics_model2, dat_ics_test)) == dat_ics_test$y2) ## 0.74
dept_model2 <- lm(y2 ~ x2, data = dat_dept_train)
mean(round(predict(dept_model2, dat_ics_test)) == dat_ics_test$y2) ## 0.75

## Root relationship
ics_model3 <- lm(y3 ~ x3, data = dat_ics_train)
mean(round(predict(ics_model3, dat_ics_test)) == dat_ics_test$y3) ## 0.74
dept_model3 <- lm(y3 ~ x3, data = dat_dept_train)
mean(round(predict(dept_model3, dat_ics_test)) == dat_ics_test$y3) ## 0.75

