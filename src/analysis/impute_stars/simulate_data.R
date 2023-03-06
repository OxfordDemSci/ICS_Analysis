# cleanup
rm(list=ls()); gc(); cat("\014"); try(dev.off(), silent=T)

# working directory
setwd(dirname(rstudioapi::getSourceEditorContext()$path))
dir.create('wd', showWarnings=FALSE)
setwd(file.path(dirname(rstudioapi::getSourceEditorContext()$path),'wd'))


#---- ics-level data ----#

# number of departments
ndept <- 200

# maximum number of case studies for a department
maxcase <- 5

# number of case studies per department
ncase <- sample(1:maxcase, size=ndept, replace=TRUE)

# ics-level data frame
dat_ics <- data.frame(dept=rep(1:ndept, ncase),
                      case=unlist(lapply(ncase, function(x)seq(1:x))))

# probability of getting 1, 2, 3, or 4 stars
prob_stars <- runif(4, 0, 1)
prob_stars <- prob_stars/sum(prob_stars)

# stars per case study
dat_ics$stars <- sample(1:4, nrow(dat_ics), replace=TRUE, prob=prob_stars)

# covariate correlated with stars (x_sd: controls correlation)
x_sd = 0.25
dat_ics$x <- scale(dat_ics$stars + rnorm(nrow(dat_ics), 0, x_sd))

plot(dat_ics$x, dat_ics$stars)


#---- dept-level data ----#

# average stars per dept
dat_dept <- aggregate(dat_ics$stars, by=list(dept=dat_ics$dept), FUN=mean)
names(dat_dept)[2] <- 'avgstars'

# number of cases per department
dat_dept$ncase <- ncase

# total stars per department
dat_dept$sumstars <- dat_dept$ncase * dat_dept$avgstars


#---- save ----#

write.csv(dat_ics, 'dat_ics.csv')
write.csv(dat_dept, 'dat_dept.csv')
