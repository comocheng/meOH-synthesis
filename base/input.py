# Data sources
database(
    thermoLibraries=['surfaceThermoPt', 'primaryThermoLibrary', 'thermo_DFT_CCSDTF12_BAC','DFT_QCI_thermo'],
    reactionLibraries = [('Surface/CPOX_Pt/Deutschmann2006', True),'BurkeH2O2inArHe','BurkeH2O2inN2'],
    seedMechanisms = [],
    kineticsDepositories = ['training'],
    kineticsFamilies =['surface','default'],
    kineticsEstimator = 'rate rules',
)

catalystProperties( # default values for Cu(111)
    bindingEnergies = {
                       'C':(-4.159, 'eV/molecule'), # from Abild-Pedersen DOI: 10.1103/PhysRevLett.99.016105
                       'O':(-3.853, 'eV/molecule'), # from Abild-Pedersen DOI: 10.1103/PhysRevLett.99.016105
                       'N':(-3.423, 'eV/molecule'), # from Katrin
                       'H':(-2.579, 'eV/molecule'), # from Katrin
                       },
    surfaceSiteDensity=(2.72e-9, 'mol/cm^2'),
)

# List of species
species(
    label='X',
    reactive=True,
    structure=adjacencyList("1 X u0"),
)

species(
    label='H2',
    reactive=True,
    structure=SMILES("[H][H]"),
)

species(
    label='CO',
    reactive=True,
    structure=SMILES("[C-]#[O+]"),
)

species(
    label='CO2',
    reactive=True,
    structure=SMILES("O=C=O"),
)

species(
    label='H2O',
    reactive=True,
    structure=SMILES("O"),
)

species(
    label='CH2O',
    reactive=True,
    structure=SMILES("C=O"),
)

species(
    label='HCOOH',
    reactive=True,
    structure=SMILES("O=CO"),
)

species(
    label='CH3OH',
    reactive=True,
    structure=SMILES("CO"),
)

species(
    label='HCOOCH3',
    reactive=True,
    structure=SMILES("O=COC"),
)

species(
   label='H*',
   reactive=True,
   structure=adjacencyList(
       """
1 H u0 p0 c0 {2,S}
2 X u0 p0 c0 {1,S}
"""),
)

species(
   label='O*',
   reactive=True,
   structure=adjacencyList(
       """
1 O u0 p2 c0 {2,D}
2 X u0 p0 c0 {1,D}
"""),
)

species(
   label='OH*',
   reactive=True,
   structure=adjacencyList(
       """
1 O u0 p2 c0 {2,S} {3,S}
2 H u0 p0 c0 {1,S}
3 X u0 p0 c0 {1,S}
"""),
)

species(
   label='H2O*',
   reactive=True,
   structure=adjacencyList(
       """
1 O u0 p2 c0 {2,S} {3,S}
2 H u0 p0 c0 {1,S}
3 H u0 p0 c0 {1,S}
4 X u0 p0 c0
"""),
)

species(
   label='CO*',
   reactive=True,
   structure=adjacencyList(
       """
1 O u0 p2 c0 {2,D}
2 C u0 p0 c0 {1,D} {3,D}
3 X u0 p0 c0 {2,D}
"""),
)

species(
   label='CO2*',
   reactive=True,
   structure=adjacencyList(
       """
1 O u0 p2 c0 {3,D}
2 O u0 p2 c0 {3,D}
3 C u0 p0 c0 {1,D} {2,D}
4 X u0 p0 c0
"""),
)

# species(
#    label='CO3*',
#    reactive=True,
#    structure=adjacencyList(
#        """
#
# """),
# )

# species(
#    label='HCO3*',
#    reactive=True,
#    structure=adjacencyList(
#        """
#
# """),
# )

species(
   label='HCO*',
   reactive=True,
   structure=adjacencyList(
       """
1 O u0 p2 c0 {2,D}
2 C u0 p0 c0 {1,D} {3,S} {4,S}
3 H u0 p0 c0 {2,S}
4 X u0 p0 c0 {2,S}
"""),
)

# species(
#    label='COH*',
#    reactive=True,
#    structure=adjacencyList(
#        """
#
# """),
# )

# species(
#    label='HCOH*',
#    reactive=True,
#    structure=adjacencyList(
#        """
# 1 O u0 p2 c0 {2,S} {4,S}
# 2 C u0 p0 c0 {1,S} {3,S} {5,D}
# 3 H u0 p0 c0 {2,S}
# 4 H u0 p0 c0 {1,S}
# 5 X u0 p0 c0 {2,D}
# """),
# )

species(
   label='HCOO*',
   reactive=True,
   structure=adjacencyList(
       """
1 O u0 p2 c0 {3,S} {5,S}
2 O u0 p2 c0 {3,D}
3 C u0 p0 c0 {1,S} {2,D} {4,S}
4 H u0 p0 c0 {3,S}
5 X u0 p0 c0 {1,S}
"""),
)

# species(
#    label='H2CO2*',
#    reactive=True,
#    structure=adjacencyList(
#        """
#
# """),
# )

species(
   label='COOH*',
   reactive=True,
   structure=adjacencyList(
       """
1 O u0 p2 c0 {3,S} {4,S}
2 O u0 p2 c0 {3,D}
3 C u0 p0 c0 {1,S} {2,D} {5,S}
4 H u0 p0 c0 {1,S}
5 X u0 p0 c0 {3,S}
"""),
)

# species(
#    label='HCOOH*',
#    reactive=True,
#    structure=adjacencyList(
#        """
#
# """),
# )

species(
   label='CH2O*',
   reactive=True,
   structure=adjacencyList(
       """
1 O u0 p2 c0 {2,D}
2 C u0 p0 c0 {1,D} {3,S} {4,S}
3 H u0 p0 c0 {2,S}
4 H u0 p0 c0 {2,S}
5 X u0 p0 c0
"""),
)

species(
   label='CH3O*',
   reactive=True,
   structure=adjacencyList(
       """
1 O u0 p2 c0 {2,S} {6,S}
2 C u0 p0 c0 {1,S} {3,S} {4,S} {5,S}
3 H u0 p0 c0 {2,S}
4 H u0 p0 c0 {2,S}
5 H u0 p0 c0 {2,S}
6 X u0 p0 c0 {1,S}
"""),
)

# species(
#    label='CH2OH*',
#    reactive=True,
#    structure=adjacencyList(
#        """
# 1 O u0 p2 c0 {2,S} {5,S}
# 2 C u0 p0 c0 {1,S} {3,S} {4,S} {6,S}
# 3 H u0 p0 c0 {2,S}
# 4 H u0 p0 c0 {2,S}
# 5 H u0 p0 c0 {1,S}
# 6 X u0 p0 c0 {2,S}
# """),
# )

species(
   label='CH3O2*',
   reactive=True,
   structure=adjacencyList(
       """
1 O u0 p2 c0 {3,S} {6,S}
2 O u0 p2 c0 {3,S} {7,S}
3 C u0 p0 c0 {1,S} {2,S} {4,S} {5,S}
4 H u0 p0 c0 {3,S}
5 H u0 p0 c0 {3,S}
6 H u0 p0 c0 {1,S}
7 X u0 p0 c0 {2,S}
"""),
)

species(
   label='CH3OH*',
   reactive=True,
   structure=adjacencyList(
       """
 1 O u0 p2 c0 {2,S} {6,S}
2 C u0 p0 c0 {1,S} {3,S} {4,S} {5,S}
3 H u0 p0 c0 {2,S}
4 H u0 p0 c0 {2,S}
5 H u0 p0 c0 {2,S}
6 H u0 p0 c0 {1,S}
7 X u0 p0 c0
"""),
)

# species(
#    label='HCOOCH3*',
#    reactive=True,
#    structure=adjacencyList(
#        """
# """),
# )

# species(
#    label='H2COOCH3*',
#    reactive=True,
#    structure=adjacencyList(
#        """
#
# """),
# )

#----------
# Reaction systems
surfaceReactor(
    temperature=(483,'K'),
    initialPressure=(15.0, 'atm'),
    initialGasMoleFractions={
        "CO": 0.1,
        "CO2": 0.1,
        "H2": 0.8,
    },
    initialSurfaceCoverages={
        "X": 1.0,
    },
    surfaceVolumeRatio=(1.e5, 'm^-1'),
    terminationConversion = { "CO":0.95,},
    terminationTime=(500., 's'),
    # terminationConversion={'O2': 0.99,},
    # terminationRateRatio=0.01
)

surfaceReactor(
    temperature=(547,'K'),
    initialPressure=(15.0, 'atm'),
    initialGasMoleFractions={
        "CO": 0.1,
        "CO2": 0.1,
        "H2": 0.8,
    },
    initialSurfaceCoverages={
        "X": 1.0,
    },
    surfaceVolumeRatio=(1.e5, 'm^-1'),
    terminationConversion = { "CO":0.95,},
    terminationTime=(500., 's'),
    # terminationConversion={'O2': 0.99,},
    # terminationRateRatio=0.01
)

surfaceReactor(
    temperature=(483,'K'),
    initialPressure=(50.0, 'atm'),
    initialGasMoleFractions={
        "CO": 0.1,
        "CO2": 0.1,
        "H2": 0.8,
    },
    initialSurfaceCoverages={
        "X": 1.0,
    },
    surfaceVolumeRatio=(1.e5, 'm^-1'),
    terminationConversion = { "CO":0.95,},
    terminationTime=(500., 's'),
    # terminationConversion={'O2': 0.99,},
    # terminationRateRatio=0.01
)

surfaceReactor(
    temperature=(547,'K'),
    initialPressure=(50.0, 'atm'),
    initialGasMoleFractions={
        "CO": 0.1,
        "CO2": 0.1,
        "H2": 0.8,
    },
    initialSurfaceCoverages={
        "X": 1.0,
    },
    surfaceVolumeRatio=(1.e5, 'm^-1'),
    terminationConversion = { "CO":0.95,},
    terminationTime=(500., 's'),
    # terminationConversion={'O2': 0.99,},
    # terminationRateRatio=0.01
)

simulator(
    atol=1e-18,
    rtol=1e-12,
)

model(
    toleranceKeepInEdge=0.0,
    toleranceMoveToCore=1e-5,
# inturrupt tolerance was 0.1 wout pruning, 1e8 w pruning on
    toleranceInterruptSimulation=1e-5,
    maximumEdgeSpecies=500000,
# PRUNING: uncomment to prune
#    minCoreSizeForPrune=50,
# prune before simulation based on thermo
#    toleranceThermoKeepSpeciesInEdge=0.5,
# prune rxns from edge that dont move into core
#    minSpeciesExistIterationsForPrune=2,
# FILTERING: set so threshold is slightly larger than max rate constants
#    filterReactions=True,
#    filterThreshold=5e8, # default value
)

options(
    units='si',
    saveRestartPeriod=None,
    generateOutputHTML=True,
    generatePlots=False,
    saveEdgeSpecies=True,
    saveSimulationProfiles=True,
)

generatedSpeciesConstraints(
    allowed=['input species','reaction libraries'],
    maximumRadicalElectrons=2,
    maximumCarbonAtoms=12,
)
