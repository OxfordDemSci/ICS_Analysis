model {

  # model
  for(d in 1:ndept){
    
    # department-level observations
    avgstars[d] ~ dnorm(mean(stars[d,1:ncase[d]]), pow(sigma, -2))
    sumstars[d] ~ dnorm(sum(stars[d,1:ncase[d]]), 1e100)

    # latent ICS-level model
    for(c in 1:ncase[d]){
      
      stars[d,c] ~ dpois(lambda[d,c]) 
      log(lambda[d,c]) = alpha + beta * x[d,c]
    }
  }
  alpha ~ dnorm(0, pow(10, -2))
  beta ~ dnorm(0, pow(10, -2))
  sigma ~ dnorm(0, 0.1) I(0,)
}
