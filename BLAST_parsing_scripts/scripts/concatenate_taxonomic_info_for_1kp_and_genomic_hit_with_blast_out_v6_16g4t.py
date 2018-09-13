#!/usr/bin/python
import sys, os, re, csv
#concatenate_taxonomic_info_for_1kp_and_genomic_hit_with_blast_output.py
#difference between v2 and previous version is that this one replaces some taxa named by Eric's Trinity assembly

#difference between v5 and v6 is that v5 fails to provide taxonomic information for gene id like
#superRosid-LMVB-2002853-Liquidambar_styraciflua, for species liquidambar

if len(sys.argv)!=2:
	print "Usage:	python concatenate_taxonomic_info_for_1kp_and_genomic_hit_with_blast_output_v2.py <blast_output_file>"
	exit()


blast_file = sys.argv[1]

def get_taxonomic_info(name):
	info = ""
	if re.match(r"^gnl\|Aquco_v1\.1", name):
		info = "Aquilegia coerulea	Viridiplantae	Basal eudicots	Ranunculales	Ranunculaceae	Aquilegia"
	if re.match(r"^gnl\|Phypa_v3\.0", name):
		info = "Physcomitrella patens	Viridiplantae	Funariidae	Funariales	Funariaceae	Physcomitrella"
	if re.match(r"^gnl\|Selmo_v1\.0\|", name):
		info = "Selaginella moellendorffii	Viridiplantae	Lycopodiidae	Selaginellales	Selaginellaceae	Selaginella"
	if re.match(r"^gnl\|Pinta_v2\.0", name):
		info = "Pinus taeda	Viridiplantae	Pinidae	Pinales	Pinaceae	Pinus"
	if re.match(r"^gnl\|Ambtr_v1\.0\.27", name):
		info = "Amborella trichopoda	Viridiplantae	Basal angiosperms	Amborellales	Amborellaceae	Amborella"
	if re.match(r"^gnl\|Spipo_v2", name):
		info = "Spirodela polyrhiza	Viridiplantae	monocots	Alismatales	Araceae	Spirodela"
	if re.match(r"^gnl\|Musac_v1\.0", name):
		info = "Musa acuminata	Viridiplantae	commelinids	Zingiberales	Musaceae	Musa"
	if re.match(r"^gnl\|Elagu_v2\.0", name):
		info = "Elaeis guineensis	Viridiplantae	commelinids	Arecales	Arecaceae	Elaeis"
	if re.match(r"^gnl\|Sorbi_v2\.1", name):
		info = "Sorghum bicolor	Viridiplantae	commelinids	Poales	Poaceae	Sorghum"
	if re.match(r"^gnl\|Orysa_v7\.0", name):
		info = "Oryza sativa	Viridiplantae	commelinids	Poales	Poaceae	Oryza"
	if re.match(r"^gnl\|Nelnu_v1\.0", name):
		info = "Nelumbo nucifera	Viridiplantae	Basal eudicots	Proteales	Nelumbonaceae	Nelumbo"
	if re.match(r"^gnl\|Vitvi_Genoscope", name):
		info = "Vitis vinifera	Viridiplantae	rosids	Vitales	Vitaceae	Vitis"
	if re.match(r"^gnl\|Eucgr_v1\.1", name):
		info = "Eucalyptus grandis	Viridiplantae	rosids	Myrtales	Myrtaceae	Eucalyptus"
	#no Egrandis
	if re.match(r"^Egrandis", name):
		info = "Eucalyptus grandis	Viridiplantae	rosids	Myrtales	Myrtaceae	Eucalyptus"
	if re.match(r"^gnl\|Phavu_v1\.0", name):
		info = "Phaseolus vulgaris	Viridiplantae	rosids	Fabales	Fabaceae	Phaseolus"
	if re.match(r"^gnl\|Medtr_Mt4\.0v1", name):
		info = "Medicago truncatula	Viridiplantae	rosids	Fabales	Fabaceae	Medicago"
	if re.match(r"^gnl\|Prupe_v1\.0", name):
		info = "Prunus persica	Viridiplantae	rosids	Rosales	Rosaceae	Prunus"
	#no Prunus_persica
	if re.match(r"^Prunus_persica", name):
		info = "Prunus persica	Viridiplantae	rosids	Rosales	Rosaceae	Prunus"
	if re.match(r"^gnl\|Carpa_ASGPBv0\.4", name):
		info = "Carica papaya	Viridiplantae	rosids	Brassicales	Caricaceae	Carica"
	if re.match(r"^gnl\|Arath_TAIR10", name):
		info = "Arabidopsis thaliana	Viridiplantae	rosids	Brassicales	Brassicaceae	Arabidopsis"
	if re.match(r"^gnl\|Theca_v1\.1", name):
		info = "Theobroma cacao	Viridiplantae	rosids	Malvales	Malvaceae	Theobroma"
	if re.match(r"^gnl\|Manes_v4\.1", name):
		info = "Manihot esculenta	Viridiplantae	rosids	Malpighiales	Euphorbiaceae	Manihot"
	#no this one "Mesculenta"
	if re.match(r"^Mesculenta_cassava", name):
		info = "Manihot esculenta	Viridiplantae	rosids	Malpighiales	Euphorbiaceae	Manihot"
	if re.match(r"^gnl\|Poptr_v3\.0", name):
		info = "Populus trichocarpa	Viridiplantae	rosids	Malpighiales	Salicaceae	Populus"
	if re.match(r"^gnl\|Betvu_v1\.1", name):
		info = "Beta vulgaris	Viridiplantae	Basal asterids	Caryophyllales	Amaranthaceae	Beta"
	#no gnl_Betvu, but only gnl|Betvu
	if re.match(r"^gnl_Betvu_v1\.1", name):
		info = "Beta vulgaris	Viridiplantae	Basal asterids	Caryophyllales	Amaranthaceae	Beta"

	if re.match(r"Caryophyllales-QAIR-\d+-Opuntia_sp\.$", name):
		info = "Opuntia sp.	Viridiplantae	Basal asterids	Caryophyllales	Cactaceae	Opuntia"
	if re.match(r"Caryophyllales-RUUB-\d+-Physena_madagascariensis", name):
		info = "Physena madagascariensis	Viridiplantae	Basal asterids	Caryophyllales	Physenaceae	Physena "
	if re.match(r"Caryophyllales-SKNL-\d+-Saponaria_officianalis", name):
		info = "Saponaria officinalis	Viridiplantae	Basal asterids	Caryophyllales	Caryophyllaceae	Saponaria"
	if re.match(r"Caryophyllales-CVDF-\d+-Simmondsia_chinensis", name):
		info = "Simmondsia chinensis	Viridiplantae	Basal asterids	Caryophyllales	Simmondsiaceae	Simmondsia"
	if re.match(r"Caryophyllales-HTDC-\d+-Tamarix_chinensis", name):
		info = "Tamarix chinensis	Viridiplantae	Basal asterids	Caryophyllales	Tamaricaceae	Tamarix"

	if re.match(r".+Kaliphora_madagascariensis$", name):
		info = "Kaliphora madagascariensis	Viridiplantae	asterids	Solanales	Montiniaceae	Kaliphora"

	if re.match(r"^gnl\|Solly_iTAGv2\.3", name):
		info = "Solanum lycopersicum	Viridiplantae	asterids	Solanales	Solanaceae	Solanum"
	if re.match(r"^gnl\|Soltu3\.4", name):
		info = "Solanum tuberosum	Viridiplantae	asterids	Solanales	Solanaceae	Solanum"
	if re.match(r"^gnl\|Utrgi_v4\.1", name):
		info = "Utricularia gibba	Viridiplantae	asterids	Lamiales	Lentibulariaceae	Utricularia"
		#no gnl_Utrgi but gnl|Utrgi
	if re.match(r"^gnl_Utrgi", name):
		info = "Utricularia gibba	Viridiplantae	asterids	Lamiales	Lentibulariaceae	Utricularia"

	if re.match(r"^gnl\|Mimgu_v2\.0", name):
		info = "Mimulus guttatus	Viridiplantae	asterids	Lamiales	Phrymaceae	Mimulus"
	if re.match(r"^gnl\|Stras_v1\.02", name):
		info = "Striga asiatica	Viridiplantae	asterids	Lamiales	Orobanchaceae	Striga"
	if re.match(r"^gnl\|Bradi1\.2", name):
		info = "Brachypodium distachyon	Viridiplantae	commelinids	Poales	Poaceae	Brachypodium"
	if re.match(r"^gnl\|Glyma1\.01", name):
		info = "Glycine max	Viridiplantae	rosids	Fabales	Fabaceae	Glycine"
	if re.match(r"^gnl\|Frave2\.0", name):
		info = "Fragaria vesca	Viridiplantae	rosids	Rosales	Rosaceae	Fragaria"
	#no Thepa
	if re.match(r"^gnl\|Thepa2\.0", name):
		info = "Thellungiella parvula	Viridiplantae	rosids	Brassicales	Brassicaceae	Arabidopsis"
	#no Phoda, good!
	if re.match(r"^gnl\|Phoda3\.0", name):
		info = "Phoenix dactylifera	Viridiplantae	commelinids	Arecales	Arecaceae	Phoenix"
	if re.match(r"^gnl_kiwi_", name):
		info = "Actinidia chinensis	Viridiplantae	asterids	Ericales	Actinidiaceae	Actinidia"
	if re.match(r".+Angelica_archangelica$", name):
		info = "Angelica archangelica	Viridiplantae	asterids	Apiales	Apiaceae	Angelica"
	if re.match(r".+Aucuba_japonica$", name):
		info = "Aucuba japonica	Viridiplantae	asterids	Garryales	Garryaceae	Aucuba"
	if re.match(r"^Coffea_Canephora", name):
		info = "Coffea canephora	Viridiplantae	asterids	Gentianales	Rubiaceae	Coffea"
	if re.match(r".+Cornus_floridana$", name):
		info = "Cornus florida	Viridiplantae	asterids	Cornales	Cornaceae	Cornus"
	if re.match(r".+Cuscuta_pentagonia$", name):
		info = "Cuscuta pentagona	Viridiplantae	asterids	Solanales	Convolvulaceae	Cuscuta"
	if re.match(r"Cuscuta_pentagona_Gunjune_\d+", name):
		info = "Cuscuta pentagona	Viridiplantae	asterids	Solanales	Convolvulaceae	Cuscuta"
	if re.match(r"^Cuscuta_pentagona_science", name):
		info = "Cuscuta pentagona	Viridiplantae	asterids	Solanales	Convolvulaceae	Cuscuta"
	if re.match(r"Cuscuta_pentagona_Neelima_\d+", name):
		info = "Cuscuta pentagona	Viridiplantae	asterids	Solanales	Convolvulaceae	Cuscuta"
	
	if re.match(r".+Convolvulus_arvensis$", name):
		info = "Convolvulus arvensis	Viridiplantae	asterids	Solanales	Convolvulaceae	Convolvulus"
	if re.match(r".+Ipomoea_coccinea$", name):
		info = "Ipomoea coccinea	Viridiplantae	asterids	Solanales	Convolvulaceae	Ipomoea"
	if re.match(r".+Ipomoea_hederacea$", name):
		info = "Ipomoea hederacea	Viridiplantae	asterids	Solanales	Convolvulaceae	Ipomoea"
	if re.match(r".+Ipomoea_indica$", name):
		info = "Ipomoea indica	Viridiplantae	asterids	Solanales	Convolvulaceae	Ipomoea"
	if re.match(r".+Ipomoea_lindheimeri$", name):
		info = "Ipomoea lindheimeri	Viridiplantae	asterids	Solanales	Convolvulaceae	Ipomoea"
	if re.match(r".+Ipomoea_lobata$", name):
		info = "Ipomoea lobata	Viridiplantae	asterids	Solanales	Convolvulaceae	Ipomoea"
	if re.match(r".+Ipomoea_nil$", name):
		info = "Ipomoea nil	Viridiplantae	asterids	Solanales	Convolvulaceae	Ipomoea"
	if re.match(r".+Ipomoea_quamoclit$", name):
		info = "Ipomoea quamoclit	Viridiplantae	asterids	Solanales	Convolvulaceae	Ipomoea"
	if re.match(r".+Ipomoea_pubescens$", name):
		info = "Ipomoea pubescens	Viridiplantae	asterids	Solanales	Convolvulaceae	Ipomoea"
	if re.match(r".+Ipomoea_purpurea.+", name):
		info = "Ipomoea_purpurea	Viridiplantae	asterids	Solanales	Convolvulaceae	Ipomoea"
	if re.match(r".+Brugmansia_sanguinea$", name):
		info = "Brugmansia sanguinea	Viridiplantae	asterids	Solanales	Solanaceae	Brugmansia"
	if re.match(r".+Atropa_belladonna$", name):
		info = "Atropa belladonna	Viridiplantae	asterids	Solanales	Solanaceae	Atropa"
	if re.match(r".+Datura_metel$", name):
		info = "Datura metel	Viridiplantae	asterids	Solanales	Solanaceae	Datura"
	if re.match(r".+Lycium_barbarum$", name):
		info = "Lycium barbarum	Viridiplantae	asterids	Solanales	Solanaceae	Lycium"


	if re.match(r".+Mansoa_alliacea$", name):
		info = "Mansoa alliacea	Viridiplantae	asterids	Lamiales	Bignoniaceae	Mansoa"
	if re.match(r".+Strobilanthes_dyerianus$", name):
		info = "Strobilanthes dyeriana	Viridiplantae	asterids	Lamiales	Acanthaceae	Strobilanthes"


	if re.match(r".+Opuntia_sp$", name):
		info = "Opuntia sp	Viridiplantae	Basal asterids	Caryophyllales	Cactaceae	Opuntia"




	if re.match(r".+Lycium_sp$", name):
		info = "Lycium sp.	Viridiplantae	asterids	Solanales	Solanaceae	Solanum"
	#no this one that has a "."
	if re.match(r".+Lycium_sp\.$", name):
		info = "Lycium sp.	Viridiplantae	asterids	Solanales	Solanaceae	Solanum"
	if re.match(r".+Lycopersicon_cheesmanii$", name):
		info = "Lycopersicon cheesmanii	Viridiplantae	asterids	Solanales	Solanaceae	Solanum"
	if re.match(r".+Nicotiana_sylvestris$", name):
		info = "Nicotiana sylvestris	Viridiplantae	asterids	Solanales	Solanaceae	Solanum"
	if re.match(r".+Solanum_dulcamara$", name):
		info = "Solanum dulcamara	Viridiplantae	asterids	Solanales	Solanaceae	Solanum"
	if re.match(r".+Solanum_lasiophyllum$", name):
		info = "Solanum lasiophyllum	Viridiplantae	asterids	Solanales	Solanaceae	Solanum"
	if re.match(r".+Solanum_ptychanthum$", name):
		info = "Solanum ptychanthum	Viridiplantae	asterids	Solanales	Solanaceae	Solanum"
	if re.match(r".+Solanum_sisymbriifolium$", name):
		info = "Solanum sisymbriifolium	Viridiplantae	asterids	Solanales	Solanaceae	Solanum"
	if re.match(r".+Solanum_xanthocarpum$", name):
		info = "Solanum xanthocarpum	Viridiplantae	asterids	Solanales	Solanaceae	Solanum"
	if re.match(r".+Vitex_agnus_castus$", name):
		info = "Vitex agnus-castus	Viridiplantae	asterids	Solanales	Solanaceae	Solanum"
	if re.match(r".+Berberidopsis_beckleri$", name):
		info = "Berberidopsis beckleri	Viridiplantae	Basal asterids	Berberidopsidales	Berberidopsidaceae	Berberidopsis"
	if re.match(r".+Helianthus_annuus.+", name):
		info = "Helianthus annuus	Viridiplantae	asterids	Asterales	Asteraceae	Helianthus"
	if re.match(r".+Lactuca_sativa.+", name):
		info = "Lactuca sativa	Viridiplantae	asterids	Asterales	Asteraceae	Lactuca"
	if re.match(r".+Lobelia_siphilitica$", name):
		info = "Lobelia siphilitica	Viridiplantae	asterids	Asterales	Campanulaceae	Lobelia"
	if re.match(r"^Phoradendron_serotinum", name):
		info = "Phoradendron serotinum	Viridiplantae	Basal asterids	Santalales	Viscaceae	Phoradendron"
	if re.match(r"^Ximenia_americana", name):
		info = "Ximenia americana	Viridiplantae	Basal asterids	Santalales	Olacaceae	Ximenia"
	if re.match(r"^Exocarpos_cupressiformis", name):
		info = "Exocarpos cupressiformis	Viridiplantae	Basal asterids	Santalales	Santalaceae	Exocarpos"
	if re.match(r"^Santalum_acuminatum", name):
		info = "Santalum acuminatum	Viridiplantae	Basal asterids	Santalales	Santalaceae	Santalum"
	if re.match(r"^Dendropemon_caribaeus", name):
		info = "Dendropemon caribaeus	Viridiplantae	Basal asterids	Santalales	Loranthaceae	Dendropemon"
	if re.match(r"^Daenikera_sp", name):
		info = "Daenikera sp.	Viridiplantae	Basal asterids	Santalales	Santalaceae	Daenikera"
	if re.match(r".+Plumbago_auriculata$", name):
		info = "Plumbago auriculata	Viridiplantae	Basal asterids	Caryophyllales	Plumbaginaceae	Plumbago"
	if re.match(r".+Scaevola_sp\.$", name):
		info = "Scaevola sp.	Viridiplantae	asterids	Asterales	Goodeniaceae	Scaevola"
	if re.match(r".+Scaevola_sp$", name):
		info = "Scaevola sp.	Viridiplantae	asterids	Asterales	Goodeniaceae	Scaevola"
	if re.match(r".+Wrightia_natalensis$", name):
		info = "Wrightia natalensis	Viridiplantae	asterids	Gentianales	Apocynaceae	Wrightia"
	if re.match(r".+Ximenia_americana$", name):
		info = "Ximenia americana	Viridiplantae	Basal asterids	Santalales	Ximeniaceae	Ximenia"
	if re.match(r"^Balanophora_fungosa", name):
		info = "Balanophora fungosa	Viridiplantae	Basal asterids	Santalales	Balanophoraceae	Balanophora"
	if re.match(r".+Illicium_floridanum$", name):
		info = "Illicium floridanum	Viridiplantae	Basal angiosperms	Austrobaileyales	Schisandraceae	Illicium"
	if re.match(r".+Nuphar_advena$", name):
		info = "Nuphar advena	Viridiplantae	Basal angiosperms	Nymphaeales	Nymphaeaceae	Nuphar"
	if re.match(r".+Buxus_sempervirens-green_branch_with_leaves$", name):
		info = "Buxus sempervirens	Viridiplantae	Basal eudicots	Buxales	Buxaceae	Buxus"
	if re.match(r".+Ceratophyllum_demersum$", name):
		info = "Ceratophyllum demersum	Viridiplantae	Basal eudicots	Ceratophyllales	Ceratophyllaceae	Ceratophyllum"
	if re.match(r".+Gunnera_manicata$", name):
		info = "Gunnera manicata	Viridiplantae	Basal eudicots	Gunnerales	Gunneraceae	Gunnera"
	if re.match(r".+Meliosma_cuneifolia$", name):
		info = "Meliosma cuneifolia	Viridiplantae	Basal eudicots	Proteales	Sabiaceae	Meliosma"
	if re.match(r".+Nandina_domestica$", name):
		info = "Nandina domestica	Viridiplantae	Basal eudicots	Ranunculales	Berberidaceae	Nandina"
	if re.match(r".+Platanus_occidentalis$", name):
		info = "Platanus occidentalis	Viridiplantae	Basal eudicots	Proteales	Platanaceae	Platanus"
	if re.match(r".+Trochodendron_araliodes$", name):
		info = "Trochodendron aralioides	Viridiplantae	Basal eudicots	Trochodendrales	Trochodendraceae	Trochodendron"
	if re.match(r".+Brassica_nigra$", name):
		info = "Brassica nigra	Viridiplantae	rosids	Brassicales	Brassicaceae	Brassica"

	if re.match(r".+Oxalis_sp\.$", name):
		info = "Oxalis sp.	Viridiplantae	rosids	Oxalidales	Oxalidaceae	Oxalis"
	if re.match(r".+Oxalis_sp$", name):
		info = "Oxalis sp.	Viridiplantae	rosids	Oxalidales	Oxalidaceae	Oxalis"

	if re.match(r"^Alectra_vogelii", name):
		info = "Alectra vogelii	Viridiplantae	asterids	Lamiales	Orobanchaceae	Alectra"
	if re.match(r"^Conopholis_americana", name):
		info = "Conopholis americana	Viridiplantae	asterids	Lamiales	Orobanchaceae	Conopholis"
	if re.match(r"^Epifagus_virginiana", name):
		info = "Epifagus virginiana	Viridiplantae	asterids	Lamiales	Orobanchaceae	Epifagus"

	if re.match(r"^Orobanche_californica", name):
		info = "Orobanche californica	Viridiplantae	asterids	Lamiales	Orobanchaceae	Orobanche"
	if re.match(r"^Orobanche_fasciculata", name):
		info = "Orobanche fasciculata	Viridiplantae	asterids	Lamiales	Orobanchaceae	Orobanche"


	if re.match(r"^Orobanche_minor", name):
		info = "Orobanche minor	Viridiplantae	asterids	Lamiales	Orobanchaceae	Orobanche"
	if re.match(r"^Phelipanche_mutelii", name):
		info = "Phelipanche mutelii	Viridiplantae	asterids	Lamiales	Orobanchaceae	Phelipanche"
	if re.match(r"^Phelipanche_ramosa", name):
		info = "Phelipanche ramosa	Viridiplantae	asterids	Lamiales	Orobanchaceae	Phelipanche"
	if re.match(r"^Striga_gesneroides", name):
		info = "Striga gesneroides	Viridiplantae	asterids	Lamiales	Orobanchaceae	Striga"
	if re.match(r"^Triphysaria_eriantha", name):
		info = "Triphysaria eriantha	Viridiplantae	asterids	Lamiales	Orobanchaceae	Triphysaria"
	if re.match(r"^Triphysaria_pusilla", name):
		info = "Triphysaria pusilla	Viridiplantae	asterids	Lamiales	Orobanchaceae	Triphysaria"

	if re.match(r"^LiPhGnB2", name):
		info = "Lindenbergia philippensis	Viridiplantae	asterids	Lamiales	Orobanchaceae	Lindenbergia"
	if re.match(r"^PhAeBC5", name):
		info = "Phelipanche aegyptiaca	Viridiplantae	asterids	Lamiales	Orobanchaceae	Phelipanche"
	if re.match(r"^StHeBC3", name):
		info = "Striga hermonthica	Viridiplantae	asterids	Lamiales	Orobanchaceae	Striga"
	if re.match(r"^TrVeBC3", name):
		info = "Triphysaria versicolor	Viridiplantae	asterids	Lamiales	Orobanchaceae	Triphysaria"

	#no this one with a dot
	if re.match(r".+Salvia_spp\.$", name):
		info = "Salvia spp.	Viridiplantae	asterids	Lamiales	Lamiaceae	Salvia"
	if re.match(r".+Salvia_spp$", name):
		info = "Salvia spp.	Viridiplantae	asterids	Lamiales	Lamiaceae	Salvia"
	if re.match(r".+Sinningia_tuberosa$", name):
		info = "Sinningia tuberosa	Viridiplantae	asterids	Lamiales	Gesneriaceae	Sinningia"
	if re.match(r"^Lavandula_angustifolia", name):
		info = "Lavandula angustifolia	Viridiplantae	asterids	Lamiales	Lamiaceae	Lavandula"


	if re.match(r".+Ehretia_acuminata$", name):
		info = "Ehretia acuminata 	Viridiplantae	asterids	Lamiales	Boraginaceae	Ehretia"
	if re.match(r".+Lonicera_japonica$", name):
		info = "Lonicera japonica 	Viridiplantae	asterids	Dipsacales	Caprifoliaceae	Lonicera"
	if re.match(r".+Ilex_paraguariensis$", name):
		info = "Ilex paraguariensis	Viridiplantae	asterids	Aquifoliales	Aquifoliaceae	Ilex"

	if re.match(r"^Olea_europaea", name):
		info = "Olea europaea	Viridiplantae	asterids	Lamiales	Oleaceae	Olea"

	if re.match(r"^Paulownia_fargesii", name):
		info = "Paulownia fargesii 	Viridiplantae	asterids	Lamiales	Paulowniaceae	Paulownia"
	if re.match(r".+Anthirrhinum_majus.+", name):
		info = "Antirrhinum majus	Viridiplantae	asterids	Lamiales	Plantaginaceae	Antirrhinum"
	if re.match(r".+Rehmannia_glutinosa$", name):
		info = "Rehmannia glutinosa	Viridiplantae	asterids	Lamiales	Rehmanniaceae	Rehmannia"
	if re.match(r".+Verbena_hastata$", name):
		info = "Verbena hastata	Viridiplantae	asterids	Lamiales	Verbenaceae	Verbena"
	if re.match(r"^Csativus_cucumber", name):
		info = "Cucumis sativus	Viridiplantae	rosids	Cucurbitales	Cucurbitaceae	Cucumis"
	if re.match(r"^Pilostyles_thunbergii", name):
		info = "Pilostyles_thunbergii	Viridiplantae	rosids	Cucurbitales	Apodanthaceae	Pilostyles"
	if re.match(r"^Csinensis\.orange", name):
		info = "Citrus sinensis	Viridiplantae	rosids	Sapindales	Rutaceae	Citrus"
	if re.match(r"^Graimondii_cotton", name):
		info = "Gossypium raimondii	Viridiplantae	rosids	Malvales	Malvaceae	Gossypium"
	if re.match(r"^Ljaponicus_lotus", name):
		info = "Lotus japonicus	Viridiplantae	rosids	Fabales	Fabaceae	Lotus"
	if re.match(r"^Mulberry_Morus", name):
		info = "Morus notabilis	Viridiplantae	rosids	Rosales	Moraceae	Morus"
	if re.match(r".+Oenothera_laciniata_evening_primrose$", name):
		info = "Oenothera laciniata	Viridiplantae	rosids	Myrtales	Onagraceae	Oenothera"

	if re.match(r".+Geranium_carolinianum$", name):
		info = "Geranium carolinianum	Viridiplantae	rosids	Geraniales	Geraniaceae	Geranium"

	if re.match(r".+Dillenia_indica$", name):
		info = "Dillenia indica	Viridiplantae	Unique rosids	Dilleniales	Dilleniaceae	Dillenia"


	if re.match(r".+Passiflora_caerulea$", name):
		info = "Passiflora caerulea	Viridiplantae	rosids	Malpighiales	Passifloraceae	Passiflora"
	if re.match(r".+Passiflora_edulis$", name):
		info = "Passiflora edulis	Viridiplantae	rosids	Malpighiales	Passifloraceae	Passiflora"
	if re.match(r".+Crossopetalum_rhacoma$", name):
		info = "Crossopetalum rhacoma	Viridiplantae	rosids	Celastrales	Celastraceae	Crossopetalum"
	if re.match(r".+Larrea_tridentata$", name):
		info = "Larrea tridentata	Viridiplantae	rosids	Zygophyllales	Zygophyllaceae	Larrea"
	if re.match(r".+Heuchera_sanguinea$", name):
		info = "Heuchera sanguinea	Viridiplantae	Basal rosids	Saxifragales	Saxifragaceae	Heuchera"
	if re.match(r".+Liquidambar_styraciflua$", name):
		info = "Liquidambar styraciflua	Viridiplantae	Basal rosids	Saxifragales	Saxifragaceae	Liquidambar"



	if re.match(r"^Pvulgaris_common_bean", name):
		info = "Phaseolus vulgaris	Viridiplantae	rosids	Fabales	Fabaceae	Phaseolus"
	if re.match(r".+Quercus_shumardii_oak$", name):
		info = "Quercus shumardii	Viridiplantae	rosids	Fagales	Fagaceae	Quercus"
	if re.match(r".+Staphylea_trifolia$", name):
		info = "Staphylea trifolia	Viridiplantae	rosids	Crossosomatales	Staphyleaceae	Staphylea"
	if re.match(r".+Acorus_americanus_monocot$", name):
		info = "Acorus americanus	Viridiplantae	monocots	Acorales	Acoraceae	Acorus"
	if re.match(r".+Dioscorea_villosa$", name):
		info = "Dioscorea villosa	Viridiplantae	monocots	Dioscoreales	Dioscoreaceae	Dioscorea"
	if re.match(r"^P\.equestris_orchid", name):
		info = "Phalaenopsis equestris	Viridiplantae	monocots	Asparagales	Orchidaceae	Phalaenopsis"
	if re.match(r"^Spolyrhiza_duckweed", name):
		info = "Spirodela polyrhiza	Viridiplantae	monocots	Alismatales	Araceae	Spirodela"
	if re.match(r".+Typha_latifolia_monocot$", name):
		info = "Typha latifolia	Viridiplantae	commelinids	Poales	Typhaceae	Typha"
	if re.match(r".+Yucca_filamentosa_monocot$", name):
		info = "Yucca filamentosa	Viridiplantae	monocots	Asparagales	Asparagaceae	Yucca"

	if re.match(r"^Amaranthus_hypochondriacus_", name):
		info = "Amaranthus hypochondriacus	Viridiplantae	Basal eudicots	Caryophyllales	Amaranthaceae	Amaranthus"
	if re.match(r"^Arabidopsis_lyrata_", name):
		info = "Arabidopsis lyrata	Viridiplantae	rosids	Brassicales	Brassicaceae	Arabidopsis"
	if re.match(r"^artichoke_", name):
		info = "Cynara cardunculus	Viridiplantae	asterids	Asterales	Asteraceae	Cynara"
	if re.match(r"^Capsella_grandiflora_", name):
		info = "Capsella grandiflora	Viridiplantae	rosids	Brassicales	Brassicaceae	Capsella"
	if re.match(r"^Cc_coffee", name):
		info = "Coffea canephora	Viridiplantae	asterids	Gentianales	Rubiaceae	Coffea"
	if re.match(r"^Cucumis_sativus_", name):
		info = "Cucumis sativus	Viridiplantae	rosids	Cucurbitales	Cucurbitaceae	Cucumis"
	if re.match(r"^Daucus_carota_", name):
		info = "Daucus carota 	Viridiplantae	asterids	Apiales	Apiaceae	Daucus"
	if re.match(r"^Cpent", name):
		info = "Cuscuta pentagona	Viridiplantae	asterids	Solanales	Convolvulaceae	Cuscuta"
	if re.match(r"^Eutrema_salsugineum_", name):
		info = "Eutrema salsugineum	Viridiplantae	rosids	Brassicales	Brassicaceae	Eutrema"
	if re.match(r"^Fraxinus_excelsior_ash_", name):
		info = "Fraxinus excelsior	Viridiplantae	asterids	Lamiales	Oleaceae	Fraxinus"
	if re.match(r"^Ipomea_trifida_", name):
		info = "Ipomea trifida	Viridiplantae	asterids	Solanales	Convolvulaceae	Ipomoea"
	if re.match(r"^gnl_kiwi_Achn", name):
		info = "Actinidia chinensis	Viridiplantae	asterids	Ericales	Actinidiaceae	Actinidia"
	if re.match(r"^Kalanchoe_marnieriana", name):
		info = "Kalanchoe marnieriana	Viridiplantae	rosids	Saxifragales	Crassulaceae	Kalanchoe"

	if re.match(r"^Kalanchoe_laxiflora", name):
		info = "Kalanchoe laxiflora	Viridiplantae	rosids	Saxifragales	Crassulaceae	Kalanchoe"

	if re.match(r"^Linum_usitatissimum", name):
		info = "Linum usitatissimum	Viridiplantae	rosids	Malpighiales	Linaceae	Linum"
	if re.match(r"^Nicotiana_benthamiana_", name):
		info = "Nicotiana benthamiana	Viridiplantae	asterids	Solanales	Solanaceae	Nicotiana"
	if re.match(r"^PhAeBC6_", name):
		info = "Phelipanche aegyptiaca	Viridiplantae	asterids	Lamiales	Orobanchaceae	Phelipanche"
	if re.match(r"^Sesamum_indicumSIN", name):
		info = "Sesamum indicum	Viridiplantae	asterids	Lamiales	Pedaliaceae	Sesamum"
	if re.match(r"^StHeBC4", name):
		info = "Striga hermonthica	Viridiplantae	asterids	Lamiales	Orobanchaceae	Striga"
	if re.match(r"^TrVeBC4", name):
		info = "Triphysaria versicolor	Viridiplantae	asterids	Lamiales	Orobanchaceae	Triphysaria"






		
	return info

with open(blast_file,"r") as f:
	for row in f:
		row = row.rstrip("\n")
		row = row.rstrip()
		row_list = row.split("\t")
		hit = row_list[1]
		try:

			print row + "\t" + get_taxonomic_info(hit)

		except:
			pass

