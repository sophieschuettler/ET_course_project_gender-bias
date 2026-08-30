library(lmerTest); library(emmeans)
d <- read.csv("data/processed/balanced_12/analysis_results.csv")
d$form    <- factor(d$form,    levels=c("masc","fem","star"))
d$anaphor <- factor(d$anaphor, levels=c("M","F"))

measures <- c("initial_fixation_duration", "go_past_duration", "regressions_in", "total_fixation_duration") 
regions  <- c("rn", "an", "spill")

sink("data/stats/analysis/stats_lmm.txt")
for (measure in measures) {
  cat("\n##################################################\n")
  cat("             MEASURE:", measure, "                  \n")
  cat("##################################################\n")
  
  for (reg in regions) {
    cat("\n=====", reg, "=====\n")
    dd <- subset(d, aoi_type == reg)
    
    formula_full <- paste(measure, "~ form * anaphor + (1 | subject) + (1 | RN)")
    m <- lmer(as.formula(formula_full), data = dd)
    
    print(anova(m))
    print(emmeans(m, pairwise ~ form))
    print(emmeans(m, pairwise ~ anaphor))
    print(emmeans(m, pairwise ~ anaphor | form))
  }
}

sink()