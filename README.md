<h1>  Prototype : Porte automatique avec reconnaissance faciale  </h1>
-Le projet a été réalisé pour rendre la porte plus protectrice.

-L'utilisateur peut utiliser son visage pour déverrouiller la porte

-facile à utiliser (attention aux chemin {l'emplacement des fichiers) ils doivent  etre correcte si vous voulez utilisé mon projet}

-Le projet a été réalisé en langage Python et en langage C dans Arduino

-Arduino a été utilisé pour montrer la démo de la porte.(montrer l'ouverture de le porte al'aide d'un servo motor)



<h1>BIBLIOTHÈQUE REQUISE</h1>

1.Open-Cv

2.Pyserial

3.Pyttsx3

4.numpy

<h1>explication de code </h1>

      ***  code : collecting data face ***
      
--   ce code capture des echantillons de visage à partir de la video capturée par la camèra 
--   il détecte les visage à l'aide d'un classificateur en cascade Haar
--   il enregistre chaque échantillon de visage dans un répertoir spécifie avec un nom de fichier unique (image pour mon cas ) 
--    le processus se repète j'usqu'un nombre spécifie d'échantillons aient été collectes


       *** code : facelockdoor***
        
  ++++++++++++++++++   les algorithemes et modèles  +++++++++++++++++

  
 --  l'algoritheme principale  est  <b> LBPH</b> [classificateur d'image pour la reconnaissance faciale ,il calcule les dimension de visage et les pixeles...]

-- Pour que LBPH fonctionne, il faut d’abord avoir le visage concerné ,pour ça on utilise un classificateur en cascade Haar qu'a le role de détecté les objet dans un image on l'utilise ici pour détecte le visage 

     **** les fonctions *****

-- face_detector(img,siz=0,5) cette fonction  prende une image en entrée et retourne une version en gray et avec un rectangle sur le visage 

--  speak(audio)  convirtir un text en discour 

--     ...

      ############  le principe de fonctionnement ####################

      -- le code récupère les images qu'on est déjà collecté ,ces images utilisé pour entrainer le modèle  afin qu'il va reconnut les visages. comme jai déjà dis  apres la récuperation des images <b>LBPH</b> passe sur ces images pour apprendre les caracteristique de chaque visage 
      -- apres l'entrainement (modèle entainé) le code commence à capturer des images de la webcame en temp réel (Photos des utilisateurs ). pour chaque image capturée le classificateur détecte les visage ,ces visage sont ensuite envoyer au modèle de reconnaissence LBPH pour la classification 
      -- si un visage est reconnu avec un confiance > 83% une communication avec l'arduino mis en oeuvre via la communication serie (l'arduino recoit "a" ==> servo -->90 ou 180 ça dépend de vous )
  
