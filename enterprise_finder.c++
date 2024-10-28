#include <iostream>
#include <fstream>
#include <sstream>
#include <string>
#include <map>
#include <vector>
#include <cstdint>

class CT_ROW {
    public:
        CT_ROW() {
            _row["CT_Siret"] = "";
            _row["CT_Num"] = "";
            _row["CT_Intitule"] = "";
            _row["DB_NAME"] = "";
        };
        ~CT_ROW()=default;
        void setrow(std::string CT_Siret, std::string CT_Num, std::string CT_Intitule, std::string DB_NAME) {
            _row["CT_Siret"] = CT_Siret;
            _row["CT_Num"] = CT_Num;
            _row["CT_Intitule"] = CT_Intitule;
            _row["DB_NAME"] = DB_NAME;
        };
        std::map<std::string, std::string> getrow() { return _row; };
    private:
        std::map<std::string, std::string> _row;
};

class CT_BASE {
    public:
        CT_BASE(){};
        ~CT_BASE()=default;
        std::vector<std::map<std::string, std::string>> getbase() { return _base; };
        void setbase(std::vector<std::map<std::string, std::string>> base) {
            for (auto& row : base)
                _base.push_back(row);
        };
        void addrow(std::map<std::string, std::string> row) { _base.push_back(row); };
        std::map<std::string, std::string> getrow(std::int64_t index) {
            return _base[index];
        };
    private:
        std::vector<std::map<std::string, std::string>> _base;
};

int main() {
    std::ifstream file("client_good_siret.csv");

    if (!file.is_open()) {
        std::cerr << "Error opening file" << std::endl;
        return 1;
    }

    std::string line;

    // Read the header line
    if (std::getline(file, line)) {
        std::cout << "Header: " << line << std::endl;
    }

    // Read data lines
    auto base = CT_BASE();
    while (std::getline(file, line)) {
        auto row = CT_ROW();
        std::istringstream ss(line);
        std::string CT_Siret, CT_Num, CT_Intitule, DB_NAME;

        // Read and split the line by commas
        std::getline(ss, CT_Siret, ',');
        std::getline(ss, CT_Num, ',');
        std::getline(ss, CT_Intitule, ',');
        std::getline(ss, DB_NAME, ',');

        row.setrow(CT_Siret, CT_Num, CT_Intitule, DB_NAME);
        base.addrow(row.getrow());
        // Print the values
    }
    file.close();
    for (auto &r : base.getbase()) {
        std::cout << "CT_Siret: " << r["CT_Siret"]
            << ", CT_Num: " << r["CT_Num"]
            << ", CT_Intitule: " << r["CT_Intitule"]
            << ", DB_NAME: " << r["DB_NAME"] << std::endl;
    }
    return 0;
}
