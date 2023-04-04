#include <cstdint>
#include <cstdio>
#include <cstring>
#include <iostream>
#include <sys/stat.h>

using File = int;
using AllocBlock = uint16_t[32];

// rozmiar 0x8
struct __attribute__((packed)) FileDesc {
  char fileName[5];           // 0x0 nazwa pliku
  uint16_t fileSize;          // 0x5 rozmiar w bajtach
  uint8_t startingBlockIndex; // 0x6 indeks pierwszej jednostki alokacji
};                            // rozmiar 0x7

// rozmiar 0x9
struct __attribute__((packed)) TransactionStatus {
  uint8_t isActive; // 0x0	czy tranzakcja jest w trakcie (jeżeli True = nie
                    // ukończona)
  char newName[5];  // 0x1	nowa nazwa
  uint16_t newSize; // 0x6	nowy rozmiar
  uint8_t descriptorIndex; // 0x8	indeks deskryptora zmienianego pliku
};

// rozmiar 0x13
struct __attribute__((packed)) ControlBlock {
  TransactionStatus transaction; // 0x0-0x9
  uint64_t usedBlocks; // 0xA-0x12	maska bitów, które bloki są w użyciu
};

// rozmiar 0x1000
struct DiskImage {
  FileDesc table[13];    // 0x0
  ControlBlock control;  // 0x68
  uint8_t unused[7];     // 0x7B stracone bajty
  AllocBlock blocks[62]; // 0x80
};

DiskImage diskImage{};

void FillExample() {

  // dane plików
  char data1[101] = {"Tutaj rozne dane pierwszego "
                     "pliku...................................................."
                     "..............."};
  char data2[81] = {"Tutaj drugi plik 1 2 3 4 5 6 7 8 9 10 11 12 13 14 15 16 "
                    "17 18 19 20 21 22 23 24 "};

  // przygotowanie plików
  // transakcja się nie dokończyła, plik "STARY" ma w deskryptorze rozmiar 40,
  // ale powinno być więcej
  FileDesc exampleFile{{'M', 'I', 'N', 'I', 'X'}, 100, 2}; // zajęte bloki 2 i 3
  FileDesc brokenFile{{'S', 'T', 'A', 'R', 'Y'}, 40, 4};
  memcpy(&diskImage.table[0], &exampleFile, sizeof(exampleFile));
  memcpy(&diskImage.table[1], &brokenFile, sizeof(brokenFile));

  memcpy(&diskImage.blocks[2 - 2], &data1, sizeof(data1));
  memcpy(&diskImage.blocks[4 - 2], &data2, sizeof(data2));

  uint64_t bitmask = 1 + 2 + 4 + 8 + 16; // domyślnie zajęte bloki 0 i 1, oraz
                                         // pliki były w 2,3,4
  ControlBlock control = {{1, {'N', 'O', 'W', 'Y', '\0'}, 80, 1},
                          bitmask}; // zmienił się rozmiar
  memcpy(&diskImage.control, &control, sizeof(control));
}

void ControllerMain() {
  TransactionStatus *status = &diskImage.control.transaction;
  // sprawdzenie, czy był błąd podczas transakcji
  if (status->isActive == 1) {
    auto brokenDescriptor = status->descriptorIndex;
    FileDesc *broken = &diskImage.table[brokenDescriptor];
    // naprawa
    memcpy(broken->fileName, status->newName,
           sizeof(TransactionStatus::newName));
    broken->fileSize = status->newSize;
    uint64_t firstBit = 1 << broken->startingBlockIndex;
    uint64_t lastBit = 1 << (broken->startingBlockIndex +
                             status->newSize / sizeof(AllocBlock));

    for (int i = firstBit; i <= lastBit; i <<= 1) {
      diskImage.control.usedBlocks |= i;
    }
    status->isActive = 0;
  }
  // teraz można korzystać z dysku
}

void UnpackToFolder(const char *folderName, DiskImage *image) {
  mkdir(folderName, 0777);
  char folderAndFile[500];
  strncpy(folderAndFile, folderName, sizeof(folderAndFile));
  size_t offset = strlen(folderName);
  folderAndFile[offset++] = '/';

  for (FileDesc file : image->table) {
    if (file.fileName[0] != '\0') {
      memcpy(folderAndFile + offset, file.fileName,
             sizeof(FileDesc().fileName));
      FILE *f = fopen(folderAndFile, "w+");
      char *fileDataStart = (char *)&image->blocks[file.startingBlockIndex - 2];
      fwrite(fileDataStart, file.fileSize, 1, f);
      fclose(f);
    }
  }
}

void Export(const char *name) {
  FILE *out = fopen(name, "w");
  fwrite(&diskImage, sizeof(diskImage), 1, out);
  fclose(out);
}

int main() {

  std::cout << "Total Disk size: " << sizeof(DiskImage) << std::endl;
  std::cout << "  Descriptor table: " << sizeof(DiskImage::table) << std::endl;
  std::cout << "  Control block: " << sizeof(DiskImage::control) << std::endl;
  std::cout << "  Unused: " << sizeof(DiskImage::unused) << std::endl;
  std::cout << "  General data: " << sizeof(DiskImage::blocks) << std::endl;
  // Przypadek, kiedy przerwano operację dopisywania do pliku
  FillExample();

  // Export("przed_naprawa.bin");
  UnpackToFolder("przed_naprawa", &diskImage);

  // kontroler się uruchamia
  ControllerMain();

  // Export("po_naprawie.bin");
  UnpackToFolder("po_naprawie", &diskImage);

  return 0;
}
