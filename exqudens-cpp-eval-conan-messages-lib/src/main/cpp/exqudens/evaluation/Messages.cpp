#include "exqudens/evaluation/Strings.hpp"
#include "exqudens/evaluation/Messages.hpp"

namespace exqudens::evaluation {

  std::string Messages::toMessage(int value) {
    Strings strings;
    std::string stringValue = strings.toString(value);
    return std::string("message: ") + stringValue;
  }

}
