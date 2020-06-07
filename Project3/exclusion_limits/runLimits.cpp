
#include "MC_Bayes.cpp+"

{

  Int_t Nmasses;
  Int_t mass;
  Double_t dummy;

  ifstream input("inputs/inputs_ee_masses.txt"); //change to ee or uu
  
  input >> Nmasses;

  Double_t* masses = new Double_t[Nmasses];

  Double_t* bkg = new Double_t[Nmasses];
  Double_t* bkgUncertainty = new Double_t[Nmasses];
  Double_t* efficiency = new Double_t[Nmasses];
  Double_t* efficiencyUncertainty = new Double_t[Nmasses];
  Double_t* Nsignal = new Double_t[Nmasses];
  Int_t* Nobs = new Int_t[Nmasses];


  for (mass = 0; mass < Nmasses; mass++) {
    input >> masses[mass];
    input >> dummy;
    input >> efficiency[mass];
    input >> efficiencyUncertainty[mass];
    input >> Nsignal[mass]; 
    input >> bkg[mass];
    input >> bkgUncertainty[mass];
    input >> Nobs[mass];
  }


  ofstream outputFile("limits.txt");


  for (mass = 0; mass < Nmasses; mass++) {

    cout << "\n----------------------------\n";
    cout << "mass = " << masses[mass] << " GeV:" << endl;
    
    Int_t Nchannels = 1;
	
    Double_t intLum = 1; //Changed from 20.28 to 1 because we want limits in terms of events rather than cross sections
    Double_t intLumUncertainty =0; //Changed from intLum*0.028 to 0 for the same reason

    cout << "\nInputs:\n";
    cout << "Int. luminosity = (" << intLum << " +/- " << intLumUncertainty << ")/fb\n";
    cout << "Background = " << bkg[mass] << " +/- " << bkgUncertainty[mass] << endl;
    cout << "Observed events = " << Nobs[mass] << endl;
    cout << "Signal efficiency = " << efficiency[mass] << " +/- " << efficiencyUncertainty[mass] << endl;

      
    Double_t background = bkg[mass]/intLum;
    Double_t backgroundUncertainty = bkgUncertainty[mass]/intLum;

    Int_t Nobserved = Nobs[mass];

    Double_t signalEfficiency = efficiency[mass];
    Double_t signalEfficiencyUncertainty = efficiencyUncertainty[mass];

	  
    Int_t Nmc = 5000;


    MC_Bayes* mcb = new MC_Bayes(Nchannels, intLum, intLumUncertainty, &background, &backgroundUncertainty, &Nobserved, Nmc, &signalEfficiency, &signalEfficiencyUncertainty, 
				   false,true,true,true);

    
    Double_t approxLimitEvts = 1.6 * TMath::Sqrt(bkgUncertainty[mass]*bkgUncertainty[mass] + bkg[mass]);
    if (approxLimitEvts < 3.0)
      approxLimitEvts = 3.0;
    Double_t step = approxLimitEvts/(efficiency[mass]*intLum)/500.0;

    
    Double_t limit = mcb->excludedSignal(step, false);
	
    cout << "\nObserved limit: " << limit << " fb" << endl;
    
    cout << "Observed limit / step = " << limit/step << endl;

    
    Double_t* exp = mcb->expectedExclusion(step,100000,false);

    cout << "\nExpected limit and bands [fb]:\n";
    cout << "-2sigma     -1sigma     median    +1sigma     +2sigma\n";
    cout << exp[0] << "     " << exp[1] << "     " << exp[2] << "     " << exp[3] << "     " << exp[4] << endl;

    
    outputFile << masses[mass] << " " << Nsignal[mass]/(efficiency[mass]*intLum) << " " << limit;
    for (Int_t k = 0; k < 5; k++)
      outputFile << " " << exp[k];
    outputFile << endl;

    delete mcb;
    delete[] exp;
  }
  cout << endl;

  outputFile.close();

  delete[] masses;
  delete[] bkg;
  delete[] bkgUncertainty;
  delete[] efficiency;
  delete[] efficiencyUncertainty;
  delete[] Nsignal;
  delete[] Nobs;
}


