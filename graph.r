# install.packages("plotly")

library(plotly)

data <- read.csv("/home/conmarap/Projects/website-fingerprinting/example-fingerprints/fingerprints.csv")
colors <- c('#4AC6B7', '#1972A4', '#965F8A', '#FF7070', '#C61951', '#FAEF44', '#DEAF69')

p <- plot_ly(data, x = ~total_number_packets, y = ~no_incoming_packets, z = ~no_outgoing_packets, color = ~domain, size = ~total_incoming_sizes, colors = colors,
             marker = list(symbol = 'circle', sizemode = 'diameter'), sizes = c(5, 150),
             text = ~paste('Domain:', domain, '<br># of packets:', total_number_packets)) %>%
  layout(title = 'Website Fingerprinting',
         scene = list(xaxis = list(title = 'Total Number of packets',
                      gridcolor = 'rgb(255, 255, 255)',
                      type = 'log',
                      zerolinewidth = 1,
                      ticklen = 5,
                      gridwidth = 2),
               yaxis = list(title = 'Number of Incoming Packets',
                      gridcolor = 'rgb(255, 255, 255)',
                      zerolinewidth = 1,
                      ticklen = 5,
                      gridwith = 2),
               zaxis = list(title = 'Number of Outgoing Packets',
                            gridcolor = 'rgb(255, 255, 255)',
                            type = 'log',
                            zerolinewidth = 1,
                            ticklen = 5,
                            gridwith = 2)),
         paper_bgcolor = 'rgb(243, 243, 243)',
         plot_bgcolor = 'rgb(243, 243, 243)')

p

