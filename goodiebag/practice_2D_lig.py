import sys
from openeye.oechem import *
from openeye.oedepict import *
from openeye.oegrapheme import *
from openeye.oedocking import *


def main(argv=[__name__]):

    itf = OEInterface()
    OEConfigure(itf, InterfaceData)
    OEConfigureImageWidth(itf, 900.0)
    OEConfigureImageHeight(itf, 600.0)
    OEConfigure2DMolDisplayOptions(itf, OE2DMolDisplaySetup_AromaticStyle)
    OEConfigureSplitMolComplexOptions(itf, OESplitMolComplexSetup_LigName)

    if not OEParseCommandLine(itf, argv):
        return 1

    iname = itf.GetString("-complex")
    oname = itf.GetString("-out")

    ifs = oemolistream()
    if not ifs.open(iname):
        OEThrow.Fatal("Cannot open input file!")

    ext = OEGetFileExtension(oname)
    if not OEIsRegisteredImageFile(ext):
        OEThrow.Fatal("Unknown image type!")

    ofs = oeofstream()
    if not ofs.open(oname):
        OEThrow.Fatal("Cannot open output file!")

    complexmol = OEGraphMol()
    if not OEReadMolecule(ifs, complexmol):
        OEThrow.Fatal("Unable to read molecule from %s" % iname)

    if not OEHasResidues(complexmol):
        OEPerceiveResidues(complexmol, OEPreserveResInfo_All)

    # Separate ligand and protein

    sopts = OESplitMolComplexOptions()
    OESetupSplitMolComplexOptions(sopts, itf)

    ligand = OEGraphMol()
    protein = OEGraphMol()
    water = OEGraphMol()
    other = OEGraphMol()

    pfilter = sopts.GetProteinFilter()
    wfilter = sopts.GetWaterFilter()
    sopts.SetProteinFilter(OEOrRoleSet(pfilter, wfilter))
    sopts.SetWaterFilter(OEMolComplexFilterFactory(OEMolComplexFilterCategory_Nothing))

    OESplitMolComplex(ligand, protein, water, other, complexmol, sopts)

    if ligand.NumAtoms() == 0:
        OEThrow.Fatal("Cannot separate complex!")

    # Perceive interactions

    asite = OEFragmentNetwork(protein, ligand)
    if not asite.IsValid():
        OEThrow.Fatal("Cannot initialize active site!")
    asite.SetTitle(ligand.GetTitle())

    OEAddDockingInteractions(asite)

    OEPrepareActiveSiteDepiction(asite)

    # Depict active site with interactions

    width, height = OEGetImageWidth(itf), OEGetImageHeight(itf)
    image = OEImage(width, height)

    cframe = OEImageFrame(image, width * 0.80, height, OE2DPoint(0.0, 0.0))
    lframe = OEImageFrame(image, width * 0.20, height, OE2DPoint(width * 0.80, 0.0))

    opts = OE2DActiveSiteDisplayOptions(cframe.GetWidth(), cframe.GetHeight())
    OESetup2DMolDisplayOptions(opts, itf)

    adisp = OE2DActiveSiteDisplay(asite, opts)
    OERenderActiveSite(cframe, adisp)

    lopts = OE2DActiveSiteLegendDisplayOptions(10, 1)
    OEDrawActiveSiteLegend(lframe, adisp, lopts)

    OEWriteImage(oname, image)

    return 0


#############################################################################
# INTERFACE
#############################################################################

InterfaceData = '''
!BRIEF [-complex] <input> [-out] <output image>

!CATEGORY "input/output options :"

  !PARAMETER -complex
    !ALIAS -c
    !TYPE string
    !KEYLESS 1
    !REQUIRED true
    !VISIBILITY simple
    !BRIEF Input filename of the protein complex
  !END

  !PARAMETER -out
    !ALIAS -o
    !TYPE string
    !REQUIRED true
    !KEYLESS 2
    !VISIBILITY simple
    !BRIEF Output filename
  !END

!END
'''

if __name__ == "__main__":
    sys.exit(main(sys.argv))

