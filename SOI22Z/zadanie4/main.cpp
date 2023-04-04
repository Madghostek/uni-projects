#include "monitor.h"
#include <array>
#include <iostream>
#include <pthread.h>
#include <queue>
#include <sstream>
#include <vector>

using Element = int;
using Queue = std::deque<Element>;

constexpr unsigned consumerCount = 3;

class MyMonitor : public Monitor {
public:
  MyMonitor() : Monitor(){};

  // Wrappers
  Element getValue(int id) {
    enter();
    Element e = _getValue(id);
    leave();
    return e;
  }

  void putValue(Element e) {
    enter();
    _putValue(e);
    leave();
  }

  void printQueue() {
    std::ostringstream os;
    os << " [";
    for (auto &el : shared_queue)
      os << el << " ,";
    os << "]\n";
    std::cout << os.str() << std::endl;
  }

private:
  // 9 and 3
  Condition notFull{}, minimumPresent{};
  Condition canConsume[consumerCount]{};
  Queue shared_queue;
  int previousId = -1;

  Element _getValue(int id) {
    Element result;

    // while loop, because we need to check the size again after waking up
    if (shared_queue.size() < 3) {
      wait(minimumPresent);
    }
    if (previousId == id) {
      // I know there are enough elements, let others know
      signal(minimumPresent);
      // check again, because it might've changed already
      if (previousId == id)
        wait(canConsume[id]); // I was reading last time, wait until
                              // something else happens. This case must
                              // be checked before any other
    }
    if (previousId == -1) {
      // dont remove the element
      result = shared_queue.front();
      previousId = id;
    } else {
      // take out the element now
      result = shared_queue.front();
      shared_queue.pop_front();
      previousId = -1;
      if (shared_queue.size() < 9) {
        signal(notFull);
      }
    }

    for (auto &condition : canConsume)
      signal(condition);

    return result;
  }

  void _putValue(Element &e) {
    while (shared_queue.size() == 9) {
      wait(notFull);
    }
    shared_queue.push_back(e);
    if (shared_queue.size() == 3)
      signal(minimumPresent);
  }
};

MyMonitor monitor{};

// show contents after finish
void PrintConsumerBuffer(std::vector<Element> &buf, int whoId) {
  std::ostringstream os;
  os << "-------CONSUMER " << whoId << " FINISH, buffer:\n[";
  for (auto &el : buf)
    os << el << ", ";
  os << "]" << std::endl;
  std::cout << os.str() << std::endl;
}

void *ConsumerThread(void *identifier) {

  int id = *(int *)identifier;
  std::vector<Element> rx{};
  for (unsigned i = 0; i < 30; ++i) {
    Element a = monitor.getValue(id);
    rx.push_back(a);

    printf("%d Reads: %d\n", id, a);
    monitor.printQueue();
  }
  PrintConsumerBuffer(rx, id);
  pthread_exit(NULL);
  return 0;
}

void *ProducentThread(void *data) {
  (void)data;

  for (unsigned i = 0; i < 100; ++i) {
    monitor.putValue(i);
    monitor.printQueue();
  }
  pthread_exit(NULL);
  return 0;
}

void CreateThreads(std::array<pthread_t, consumerCount> &consumers,
                   pthread_t *producent) {
  std::array<int, consumerCount> identifiers{0, 1, 2};
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

  return 0;
}