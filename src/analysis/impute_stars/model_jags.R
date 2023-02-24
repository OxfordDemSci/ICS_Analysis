# cleanup
rm(list=ls()); gc(); cat("\014"); try(dev.off(), silent=T)

# load libraries
library(runjags)
library(coda)

# working directory
setwd(dirname(rstudioapi::getSourceEditorContext()$path))
dir.create('wd', showWarnings=FALSE)
setwd(file.path(dirname(rstudioapi::getSourceEditorContext()$path),'wd'))

# load data
dat_ics <- read.csv('dat_ics.csv')
dat_dept <- read.csv('dat_dept.csv')

ndept <- nrow(dat_dept)
ncase <- dat_dept$ncase
maxcase <- max(dat_dept$ncase)


#---- jags ----#

# reshape covariate to ragged matrix
x <- matrix(NA, nrow=ndept, ncol=maxcase)
for(i in 1:nrow(x)){
  x[i,1:ncase[i]] <- as.vector(dat_ics[dat_ics$dept==i, 'x'])
}

# jags data
md <- list(ndept = nrow(dat_dept),
           ncase = dat_dept$ncase,
           avgstars = round(dat_dept$avgstars, 1),
           sumstars = dat_dept$sumstars,
           x = x
           )

# mcmc config
chains <- 3
adapt <- 1e3
warmup <- 1e3
iter <- 5e3
thin <- 1

# monitor
pars <- c('stars', 
          'lambda', 'p', 
          'alpha', 'beta', 'sigma')

# mcmc
fit <- run.jags(model = '../models/binomial.jags.R',
               monitor = pars,
               data = md,
               n.chains = chains,
               # inits = init,
               thin = thin,
               adapt = adapt,
               burnin = warmup,
               sample = iter,
               summarise = F,
               # keep.jags.files = TRUE,
               method = 'parallel'
)

# traceplots
traceplot(fit$mcmc)

# fit data.frame
fit_df <- fit$mcmc[[1]]
for(i in 2:length(fit$mcmc)){
  fit_df <- rbind(fit_df, fit$mcmc[[i]])
}


# assess fit (department-level count of stars)
test <- data.frame(dept=1:ndept)

for(i in 1:nrow(test)){
  d <- test[i,'dept']
  
  cols <- paste0('stars[',d,',',1:ncase[d],']')
  
  # true counts of x-star ICS in each department
  test[i, 'stars1'] <- sum(dat_ics[dat_ics$dept==d, 'stars']==1)
  test[i, 'stars2'] <- sum(dat_ics[dat_ics$dept==d, 'stars']==2)
  test[i, 'stars3'] <- sum(dat_ics[dat_ics$dept==d, 'stars']==3)
  test[i, 'stars4'] <- sum(dat_ics[dat_ics$dept==d, 'stars']==4)
  
  # estimated counts of x-star ICS for each department
  if(length(cols) == 1){
    test[i, 'stars1_hat'] <- sum(mean(fit_df[,cols])==1)
    test[i, 'stars2_hat'] <- sum(mean(fit_df[,cols])==2)
    test[i, 'stars3_hat'] <- sum(mean(fit_df[,cols])==3)
    test[i, 'stars4_hat'] <- sum(mean(fit_df[,cols])==4)
  } 
  else {
    test[i, 'stars1_hat'] <- sum(apply(fit_df[,cols], 2, mean)==1)
    test[i, 'stars2_hat'] <- sum(apply(fit_df[,cols], 2, mean)==2)
    test[i, 'stars3_hat'] <- sum(apply(fit_df[,cols], 2, mean)==3)
    test[i, 'stars4_hat'] <- sum(apply(fit_df[,cols], 2, mean)==4)
  }
}

mean(test$stars1==test$stars1_hat)
mean(test$stars2==test$stars2_hat)
mean(test$stars3==test$stars3_hat)
mean(test$stars4==test$stars4_hat)


# assess fit (ics-level predictions)
for(i in 1:nrow(dat_ics)){
  d <- dat_ics[i, 'dept']
  c <- dat_ics[i, 'case']
  col <- paste0('stars[', d, ',', c, ']')
  dat_ics[i, 'stars_hat'] <- mean(fit_df[,col])
}

mean(dat_ics$stars==dat_ics$stars_hat)
mean(dat_ics$stars-dat_ics$stars_hat)
mean(abs(dat_ics$stars-dat_ics$stars_hat))

hist(dat_ics$stars-dat_ics$stars_hat)

