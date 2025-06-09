#include <correction.h>
#include <TRandom3.h>
#include <string>

class EleScaSmear {
public:
  EleScaSmear(std::string json);

  double pt_smearing(std::string var, double eta, double r9, double pt);
  double pt_smearing_UP(std::string var, double eta, double r9, double pt);
  double pt_smearing_DOWN(std::string var, double eta, double r9, double pt);
  double pt_scale(std::string var, double gain, int run, double eta, double r9, double pt);
  double pt_scale_UP(std::string var, double gain, double run, double eta, double r9, double pt);
  double pt_scale_DOWN(std::string var, double gain, double run, double eta, double r9, double pt);

private:
//  double get_k(double eta, std::string var);
//  double get_std(double pt, double eta, float nL);
//  double get_rndm(double eta, float nL);

  std::unique_ptr<correction::CorrectionSet> cset;
  TRandom3 rng;
};
