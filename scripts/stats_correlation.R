d <- read.csv("data/processed/balanced_12/analysis_results.csv")
d <- subset(d, aoi_type == "an")          

# --- per-subject anaphor difference (M - F) within one form ---
subject_diff <- function(d, measure, form_lvl) {
  dd <- d[d$form == form_lvl, ]
  a  <- aggregate(dd[[measure]],
                  list(subject=dd$subject, anaphor=dd$anaphor),
                  mean, na.rm=TRUE)
  names(a)[3] <- "m"
  m <- a[a$anaphor=="M", c("subject","m")]; names(m)[2] <- "M"
  f <- a[a$anaphor=="F", c("subject","m")]; names(f)[2] <- "F"
  out <- merge(m, f, by="subject")
  out$diff <- out$M - out$F                
  out[, c("subject","diff")]
}


exposure <- unique(d[, c("subject","exposure_use","exposure_percept")])

# --- initial fixation, masculine form (the male-bias effect lived here) ---
fp <- merge(subject_diff(d, "initial_fixation_duration", "masc"), exposure, by="subject")
# --- go-past, star form (the star asymmetry lived here) ---
gp <- merge(subject_diff(d, "go_past_duration",   "star"), exposure, by="subject")

sink("data/stats/analysis/stats_correlation.txt")

cat("\n=== Initial-fixation (masc form): anaphor M-F diff vs exposure ===\n")
cat("-- self-use --\n");    print(cor.test(fp$exposure_use,     fp$diff))
cat("-- perceived --\n");   print(cor.test(fp$exposure_percept, fp$diff))

cat("\n=== Go-past (star form): anaphor M-F diff vs exposure ===\n")
cat("-- self-use --\n");    print(cor.test(gp$exposure_use,     gp$diff))
cat("-- perceived --\n");   print(cor.test(gp$exposure_percept, gp$diff))

sink()

# --- scatter plots  ---
png("plots/analysis/balanced_12/stats/corr_use.png", width=1000, height=500)
par(mfrow=c(1,2))
plot(fp$exposure_use, fp$diff, pch=19,
     xlab="Self-use Frequency of Gender Inclusive Language", ylab="Initial-fixation M-F (ms)", main="Masculine Form")
abline(lm(diff ~ exposure_use, fp), col="#1f77b4")
plot(gp$exposure_use, gp$diff, pch=19,
     xlab="Self-use Frequency of Gender Inclusive Language", ylab="Go-past M-F (ms)", main="Star Form")
abline(lm(diff ~ exposure_use, gp), col="#1f77b4")

  
png("plots/analysis/balanced_12/stats/corr_percept.png", width=1000, height=500)
par(mfrow=c(1,2))
plot(fp$exposure_percept, fp$diff, pch=19,
     xlab="Perception Frequency of Gender Inclusive Language", ylab="Initial-fixation M-F (ms)", main="Masculine Form")
abline(lm(diff ~ exposure_percept, fp), col="#1f77b4")
plot(gp$exposure_percept, gp$diff, pch=19,
     xlab="Perception Frequency of Genfer Inclusive Language", ylab="Go-past M-F (ms)", main="Star Form")
abline(lm(diff ~ exposure_percept, gp), col="#1f77b4")

dev.off()