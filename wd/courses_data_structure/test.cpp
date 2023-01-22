#include <iostream>
#include <fstream>
#include <string>
#include <poppler/cpp/poppler-document.h>
#include <poppler/cpp/poppler-page.h>
#include <poppler/cpp/poppler-page-renderer.h>
#include <poppler/cpp/poppler-rectangle.h>
#include <poppler/cpp/poppler-table.h>
#include <csv/csv.h>

int main() {
  // Open the PDF file
  poppler::document *doc = poppler::document::load_from_file("b-arch-design-S1-2023-FINAL.pdf");
  if (!doc) {
    std::cerr << "Error opening PDF file" << std::endl;
    return 1;
  }

  // Open the CSV file for writing
  io::CSVWriter writer("data.csv");

  // Iterate over the pages in the PDF
  for (int i = 0; i < doc->pages(); ++i) {
    // Get the current page
    poppler::page *page = doc->create_page(i);
    if (!page) {
      std::cerr << "Error getting page " << i << std::endl;
      continue;
    }

    // Extract the tables from the page
    std::vector<poppler::table *> tables = page->tables();
    for (const poppler::table *table : tables) {
      // Iterate over the rows and cells in the table
      for (int row = 0; row < table->rows(); ++row) {
        std::vector<std::string> cells;
        for (int col = 0; col < table->columns(); ++col) {
          // Get the cell text
          cells.push_back(table->cell_text(row, col).to_latin1());
        }
        // Write the row to the CSV file
        writer.write_row(cells);
      }
    }
    delete page;
  }
  delete doc;

  return 0;
}
