#include "monitor.h"
#include <array>
#include <iostream>
#include <pthread.h>
#include <queue>
#include <vector>

using Element = int;
using Queue = std::deque<Element>;

constexpr unsigned consumerCount = 3;
std::array<int, consumerCount> identifiers{0, 1, 2};

//***debug***
Semaphore printMutex{1}; // don't let threads print inbetween prints

class Buffer {
public:
  Buffer() : shared_queue() {}

  void putValue(Element e) {

    full.p(); // if not 0, then there is space left

    usingQueue.p();

    shared_queue.push_back(e);

    printMutex.p();
    std::cout << "P : " << e;
    printQueue();
    printMutex.v();

    if (shared_queue.size() > 3)
      empty.v();

    usingQueue.v();
  }

  Element getValue(int id) {
    // outside of critial section
    dontReadTwice[id].p(); // did it read current element already?

    empty.p();

    usingQueue.p(); // enters critical section

    auto result = getQueueElement(id);

    printMutex.p();
    std::cout << id << " : " << result;
    printQueue();
    printMutex.v();

    usingQueue.v();
    return result;
  }

  void printQueue() {
    std::cout << " [";
    for (auto &el : shared_queue)
      std::cout << el << " ,";
    std::cout << "]\n";
  }

private:
  // Everything that is private is going to be accessed only in critical
  // sections
  Queue shared_queue;

  int whoTookFirst = -1; // index into identifiers

  //***general***

  // critical section
  // only one thread at a time operates on queue
  Semaphore usingQueue{1};

  //***counting***
  Semaphore full{9};  // how many max elements
  Semaphore empty{0}; // raised when more than 3 elements in buffer

  std::array<Semaphore, consumerCount> dontReadTwice{1, 1, 1};

  Element getQueueElement(int id) {
    Element result = shared_queue.front();
    if (whoTookFirst >= 0) {
      shared_queue.pop_front();

      // increase element count
      full.v();

      // bring back up mutex of the consumer that took the element first
      dontReadTwice[whoTookFirst].v();
      // and my own too
      dontReadTwice[id].v();
      whoTookFirst = -1;
    } else {
      empty.v(); // element not taken out
      whoTookFirst = id;
    }
    return result;
  }
};

Buffer buffer{};

void PrintConsumerBuffer(std::vector<Element> &buf) {
  printMutex.p();
  std::cout << "-------CONSUMER FINISH, buffer:\n[";
  for (auto &el : buf)
    std::cout << el << ", ";
  std::cout << "]" << std::endl;
  printMutex.v();
}

void *ConsumerThread(void *identifier) {

  int id = *(int *)identifier;
  std::vector<Element> rx{};
  for (unsigned i = 0; i < 30; ++i) {
    Element a = buffer.getValue(id);
    rx.push_back(a);
  }
  PrintConsumerBuffer(rx);
  pthread_exit(NULL);
  return 0;
}

void *ProducentThread(void *data) {
  (void)data;

  for (unsigned i = 0; i < 100; ++i) {
    buffer.putValue(i);
  }
  printMutex.p();
  std::cout << "-------PRODUCENT FINISH, buffer:\n";
  buffer.printQueue();
  printMutex.v();
  pthread_exit(NULL);
  return 0;
}

void CreateThreads(std::array<pthread_t, consumerCount> &consumers,
                   pthread_t *producent) {
  // create consumers
  for (unsigned i = 0; i < consumers.size(); ++i) {
    auto res =
        pthread_create(&consumers[i], NULL, ConsumerThread, &identifiers[i]);
    if (res != 0)
      std::cerr << "thread error\n";
  }
  // create one producent
  pthread_create(producent, NULL, ProducentThread, nullptr);
}

int main() {

  // create
  std::array<pthread_t, consumerCount> consumers{};
  pthread_t producent;
  CreateThreads(consumers, &producent);

  // wait
  for (pthread_t id : consumers)
    pthread_join(id, NULL);
  pthread_join(producent, NULL);

  std::cout << "program end, buffer:";
  buffer.printQueue();

  return 0;
}