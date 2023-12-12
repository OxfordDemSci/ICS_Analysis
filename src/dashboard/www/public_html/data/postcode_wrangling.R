# cleanup
rm(list=ls()); gc(); cat("\014"); try(dev.off(), silent=T)

# working directory
setwd(dirname(rstudioapi::getSourceEditorContext()$path))

# libraries
library(sf)

# load data
postcode_v1 <- sf::st_read('UK_postcode_area.geojson')
postcode_v6 <- sf::st_read('UK_postcode_area_v6.geojson')

# postcodes missing from v6
missing_postcodes <- c()
for(pcode in postcode_v1$pc_area){
  if(!pcode %in% postcode_v6$pc_area){
    missing_postcodes <- c(missing_postcodes, pcode)
  }
}
missing_postcodes <- unique(missing_postcodes)

# append missing postcodes from v1
postcode <- rbind(postcode_v6,
                  postcode_v1[postcode_v1$pc_area %in% missing_postcodes, names(postcode_v6)])

# check that no postcodes are now missing
missing_postcodes_final <- c()
for(pcode in postcode_v1$pc_area){
  if(!pcode %in% postcode$pc_area){
    missing_postcodes_final <- c(missing_postcodes_final, pcode)
  }
}
missing_postcodes_final <- unique(missing_postcodes_final)

# save result
sf::st_write(postcode, dsn='UK_postcode_area_v7.geojson')

