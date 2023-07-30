tuto exemple concret:

tuto exemple concret:

montrer des acointances idéologiques

tuto par exemple concret:

après avoir fait un timelapse et obtenu quelques images de l'ensemble du canva via la commande suivante et les options pixel_rate et name:

	python main.py pixel_rate 2000000 name timelapse

	(cette commande enregistrera une image tous les 2 millions de pixels posés et les placera dans le dossier img sous le nom «timelapse» suivi de la date de pose du dernier pixel de l'image)

on repere sur l'une de ces image un rubiks cube et se demande bien quels interets autres peuvent bien avoir les adorateurs de rubiks cube et les haïsseurs de rubiks cube, on se munit donc de notre logiciel de retouche d'image préféré (par exemple gimp) pour obtenir les coordonnées du-dit cube.

ici le cube se trouve aux coordonnées 377-967 et fait une taille de 28 par 27 pixels (on utilisera pour le script des coordonnées absolues pour faciliter les mesures avec les logiciels de retouches, elles ne correspondront donc pas aux coordonnées de r.place ou le coin supèrieur gauche est en coordonnées négatives.

on décide donc de lancer un nouveau timelapse cette fois ci plus précis au niveau temporel mais se concentrant uniquement sur cette zone

	python main.py pixel_rate 500 name rubik zone 377 967 28 27

	(cette commande enregistrera une image tous les 500 pixels posés dans la zone 377+967_28*27 et la placera dans le dossier img sous le nom «rubik» suivi de la date de pose du dernier pixel de l'image)

on a donc 13 images de l'évolution du cube, en les parcourant on voit que ce dernier n'a pas changé de design le 25 juillet entre 13:09 et 23:53 mais a subit quelques dégats. ce dernier étant en bon état sur l'image "rubik - 2023-07-24 13:09:53.993 .png" on s'en servira de référence, on éffacera ce qui ne fait pas partie de l'œuvre et l'enregistrera autre part, par exemple dans le dossier principal du programme sous le nom "rubik_reference.png"

`il est aussi possible pour les œuvres ayant plus muttées et plus durées de prendre la référence finale et la référence de départ et d'en faire la différence (par exemple sur gimp en les ouvrant dans deux layers et en faisant filters = animation = optimize (Difference)`

en utilisant cette référence on va désormais pouvoir optenir une liste d'identifiants utilisateurices (cryptés mais exploitables pour ce que l'on veut faire maintenant) par éxemple pour savoir qui l'a défendu

	python main.py compare rubik_reference.png time_slot "2023-07-24 13:10" "2023-07-24 23:50" save_id rubik_defenders.txt

	(cette commande enregistrera le nombre de pixel de la même couleur que la référence fournie posés par chaque utilisateurice entre les dates fournies, et l'enregistrera dans le fichier rubik_defenders.txt
	

	IMPORTANT !!!!!
	vous pouvez ajouter l'option zone utilisée précédemment avec les même valeur pour gagner en temps de traitement, je ne l'ai pas mise ici pour ne pas surcharger visuellement et que vous voyez les nouvelles options utilisées, mais je recommande de le faire

	python main.py compare rubik_reference.png time_slot "2023-07-24 13:10" "2023-07-24 23:50" save_id rubik_defenders.txt zone 377 967 28 27

	)

si au contraire se sont les personnes qui ont attaquées le cube dont le comportement vous interesse vous pouvez utiliser l'option reverse_compare de la même façon

	python main.py reverse_compare rubik_reference.png time_slot "2023-07-24 13:10" "2023-07-24 23:50" save_id rubik_destroyers.txt zone 377 967 28 27

	(cette commande enregistrera le nombre de pixel de couleur différente à la référence fournie posés par chaque utilisateurice entre les dates fournies, et l'enregistrera dans le fichier rubik_destroyers.txt)

vous pouvez désormais voir ce que ces deux groupes de personnes ont fait d'autre sur le canva via l'option use_id, le nombre que vous fournirez après le fichier permettra de dire combien de pixels remplissant les conditions demandées précédements sont nécéssaires pour déclencher le suivi, par exemple

	python main.py use_id rubik_destroyers.txt 1 pixel_rate 10000 name destroyers

	(cette commande enregistrera une image tous les 10 000 pixels posés par des personnes ayant attaqué au moins UNE fois le cube et les placera dans le dossier img sous le nom «destroyers» suivi de la date de pose du dernier pixel de l'image)

	python main.py use_id rubik_defenders.txt 5 pixel_rate 10000 name defenders

	(cette commande enregistrera une image tous les 10 000 pixels posés par des personnes ayant défendu au moins CINQ fois le cube et les placera dans le dossier img sous le nom «defenders» suivi de la date de pose du dernier pixel de l'image)

les images fournies étant en transparences vous pouvez les supperposer avec une référence obtenue plus tôt pour voir plus clairement à quoi ont participé ces groupes, vous remarquerez aussi dans les deux cas des faux positif, c'est ici qu'entrent en jeu deux choses, premièrement le nombre de pixel de référence (le chiffre fourni après le fichier à l'option use_id, mais aussi les deux autres scripts présents dans le dossier, les scripts diff et add vous pourrez par exemple retirer les identifiants présents dans un fichier s'ils sont dans un autre avec la commande diff.py

	python diff.py rubik_destroyers.txt rubik_defenders.txt real_destroyers.txt

	(cette commande créra un fichier real_destroyers en ne conservant que les entrées présente dans rubik_destroyers mais pas dans rubik_defenders)

	python add.py rubik_destroyers.txt rubik_defenders.txt everybody.txt

	(cette commande créra un fichier everybody en additionnant les entrées présente dans rubik_destroyers et dans rubik_defenders)

