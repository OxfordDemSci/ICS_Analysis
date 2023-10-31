model {

  # model
  for(d in 1:ndept){
    
    # department-level observations
    avgstars[d] ~ dnorm(mean(stars[d,1:ncase[d]]), pow(sigma, -2))
    sumstars[d] ~ dnorm(sum(stars[d,1:ncase[d]]), 1e100)

    # latent ICS-level model
    for(c in 1:ncase[d]){
      
      stars[d,c] ~ dround(stars_cont[d,c], 0)
      stars_cont[d,c] ~ dunif(1, 4)
    }
  }
  sigma ~ dnorm(0, 1) I(0,)
}
