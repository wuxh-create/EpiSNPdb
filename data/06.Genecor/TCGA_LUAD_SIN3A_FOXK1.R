# ========== Plot correlation scatter plot for FOXK1 and SIN3A ==========

rm(list = ls())
gc()
# Parameter setting
Cond1 <- "LUAD"
Cond2 <- "Lung"
gene1 <- "FOXK1"
gene2 <- "SIN3A"

# Load required libraries
library(data.table)
library(dplyr)
library(ggplot2)
library(ggpubr)

file1 <- "/home/wuxh/TCGA/TCGA_exp/TCGA_LUAD_SIN3A_FOXK1.expression"
TCGA_SIN3A_FOXK1.expression <- fread(file1, header = TRUE)

# Plotting function
gene_cor_plot <- function(g1, g2, expr_data, output_dir) {
  if (is.data.table(expr_data)) expr_data <- as.data.frame(expr_data)
  
  gene1_expr <- expr_data[expr_data[, 1] == g1, ]
  gene2_expr <- expr_data[expr_data[, 1] == g2, ]
  if (nrow(gene1_expr) == 0 || nrow(gene2_expr) == 0) stop("Gene not found in expression matrix")
  
  gene1_values <- as.numeric(unlist(gene1_expr[1, -1]))
  gene2_values <- as.numeric(unlist(gene2_expr[1, -1]))
  gene1_log <- log2(gene1_values + 1)
  gene2_log <- log2(gene2_values + 1)
  
  gene_log_t <- data.frame(gene1 = gene1_log, gene2 = gene2_log)
  cor_result <- cor.test(gene1_log, gene2_log, method = "spearman", exact = FALSE)
  
  cc <- signif(cor_result$estimate, 2)
  pp <- ifelse(cor_result$p.value < 0.01,
               formatC(cor_result$p.value, format = "e", digits = 2),
               sprintf("%.2f", cor_result$p.value))
  n_sample <- nrow(gene_log_t)
  
  p <- ggscatter(gene_log_t, x = "gene1", y = "gene2",
                 color = "#FF8C00", shape = 20, size = 2.5,
                 add = "reg.line",
                 add.params = list(color = "blue", fill = "lightgray"),
                 conf.int = TRUE) +
    xlab(bquote('Expression of '*.(g1)~''~log[2](FPKM+1))) +
    ylab(bquote('Expression of '*.(g2)~''~log[2](FPKM+1))) +
    border("black") +
    labs(title = bquote('R'['spearman'] == .(cc) ~','~ 'P'['spearman'] == .(pp) ~','~ 'N' == .(n_sample))) +
    theme(plot.title = element_text(hjust = 0.5))
  
  if (!dir.exists(output_dir)) dir.create(output_dir, recursive = TRUE)
  ggsave(paste0(output_dir, "/", Cond1, "_", Cond2, "_", g1, "_", g2, ".pdf"), p, width = 6, height = 5)
  ggsave(paste0(output_dir, "/", Cond1, "_", Cond2, "_", g1, "_", g2, ".png"), p, width = 6, height = 5)
  
  cat("Gene:", g1, "vs", g2, "\n")
  cat("Spearman R =", cc, "  P =", pp, "\n")
  return(list(cor = cor_result$estimate, pvalue = cor_result$p.value))
}

# Execute plotting and correlation calculation
plot_dir <- paste0("/home/wuxh/TCGA/TCGA_exp/", Cond1, "_", Cond2)
result <- gene_cor_plot(gene1, gene2, TCGA_SIN3A_FOXK1.expression, plot_dir)

# Output result
print(result)
