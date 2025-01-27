library(ggplot2)
data = read.csv("../../data/medal_efficiency.csv")
plot(data$Medals, data$Participants)

ggplot(data, aes(x = Participants, y = Medals)) +
  geom_point(size = 3, color = "steelblue1", shape = 16) +  # Customize point size, color, and shape
  labs(
    title = "Scatterplot of Medals vs Participants",
    x = "Number of Participants",
    y = "Number of Medals"
  ) +
  theme_minimal(base_size = 15) +  # Use a clean minimal theme with adjusted font size
  theme(
    plot.title = element_text(hjust = 0.5, face = "bold", color = "darkblue"),  # Center and style the title
    axis.title.x = element_text(face = "italic", color = "darkred"),  # Style x-axis label
    axis.title.y = element_text(face = "italic", color = "darkred")  # Style y-axis label
  )

