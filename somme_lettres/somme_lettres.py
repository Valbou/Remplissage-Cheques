#!/usr/bin/env python3
# -*- coding: utf-8 -*-


class SommeVersLettres:
    """Converti une somme (float) en lettres (utilisé notamment pour les chèques et les bulletins de soutien)"""

    nombre = 0
    dico = {
        "00": "",
        "0": "zéro",
        "1": "un",
        "01": "un",
        "2": "deux",
        "02": "deux",
        "3": "trois",
        "03": "trois",
        "4": "quatre",
        "04": "quatre",
        "5": "cinq",
        "05": "cinq",
        "6": "six",
        "06": "six",
        "7": "sept",
        "07": "sept",
        "8": "huit",
        "08": "huit",
        "9": "neuf",
        "09": "neuf",
        "10": "dix",
        "11": "onze",
        "12": "douze",
        "13": "treize",
        "14": "quatorze",
        "15": "quinze",
        "16": "seize",
        "17": "dix-sept",
        "18": "dix-huit",
        "19": "dix-neuf",
        "20": "vingt",
        "30": "trente",
        "40": "quarante",
        "50": "cinquante",
        "60": "soixante",
        "80": "quatre-vingt",
    }

    def conversion(self, nombre: float, monnaie: str = "euro"):
        self.nombre = nombre
        self.monnaie = monnaie
        self.nombre = round(self.nombre, 2)
        return self._demembrement().strip()

    def _segmentation(self, entiere: str) -> list:
        """Découpe un nombre en sous-nombre de 3 chiffres"""
        liste_nombre = []
        seg_num = ""
        for i in entiere[::-1]:
            seg_num += i
            # Création des blocs de 3 chiffres
            if len(seg_num) == 3:
                liste_nombre.append("".join(seg_num[::-1]))
                seg_num = ""
        if len(seg_num):  # Récupération du reste (inférieur à 3 chiffres)
            liste_nombre.append("{:0>3}".format("".join(seg_num[::-1])))
        return liste_nombre

    def _traitement_segment(self, liste_nombre, mantisse):
        """Converti chaque sous-nombre individuellement en lettres"""
        liste_noms = [self._nom_dizaine(mantisse, is_mantisse=True)]
        for i in liste_nombre:
            centaine = self._nom_centaine(i)
            dizaine = self._nom_dizaine(i)
            if centaine and dizaine:
                liste_noms.append(centaine + "-" + dizaine)
            elif centaine:
                liste_noms.append(centaine)
            else:
                liste_noms.append(dizaine)
        return liste_noms

    def _demembrement(self):
        """Démembre le nombre en sous-nombres à 3 chiffres"""
        n_str = str(self.nombre)
        entiere, mantisse = n_str.split(".", 1)

        # Evite que : 0.1 ne devienne 1 centime au lieu de 10 centimes
        mantisse = f"{mantisse:0<2}"
        liste_nombre = self._segmentation(entiere)
        liste_noms = self._traitement_segment(liste_nombre, mantisse)
        return self._nom_puissances(liste_noms)

    def _nom_dizaine(self, nombre: str, is_mantisse: bool = False):
        """Génère la dizaine et l'unité d'un nombre à 3 chiffres"""

        # Recadrage de la partie à traiter selon la partie du nombre
        if is_mantisse:
            nombre = "{:0<2}".format(nombre)
        else:
            nombre = "{:0>3}".format(nombre)[-2:]

        # Traitement des dizaines
        if nombre in self.dico:
            return self.dico[nombre]
        elif int(nombre) > 80:
            return self.dico["80"] + "-" + self.dico[str(int(nombre) - 80)]
        elif int(nombre) > 60:
            if nombre == "61" or nombre == "71":
                return self.dico["60"] + "-et-" + self.dico[str(int(nombre) - 60)]
            else:
                return self.dico["60"] + "-" + self.dico[str(int(nombre) - 60)]
        elif int(nombre) > 20:
            diz = str(nombre)[:1] + "0"
            if int(nombre) - int(diz) == 1:
                return self.dico[diz] + "-et-" + self.dico[str(int(nombre) - int(diz))]
            return self.dico[diz] + "-" + self.dico[str(int(nombre) - int(diz))]

        # Cas particulier (non géré)
        return ""

    def _nom_centaine(self, nombre: str):
        """Génère la centaine d'un nombre à 3 chiffres"""
        nombre = "{:0>3}".format(nombre)[:1]
        if nombre == "0":
            return ""
        elif nombre == "1":
            return "cent"
        else:
            return self.dico[nombre] + "-cent"

    def _nom_puissances(self, liste_noms: list):
        """Génère les noms des puissances de 3 (milliers, millions etc...)"""
        liste = ["centimes", self.monnaie, "mille", "millions", "milliards"]
        final = ""
        for i, mot in enumerate(liste_noms):
            if i % 5 == 0 and mot:
                final = "et " + mot + " " + liste[i % 5]
            elif i % 5 in [1, 3, 4]:
                final = mot + ("-" if i % 5 == 3 else " ") + liste[i % 5] + " " + final
            elif i % 5 == 2:
                if mot and mot not in "un":
                    print("cas 1 :", mot)
                    final = mot + "-" + liste[i % 5] + " " + final
                elif mot and mot in "un":
                    print("cas 2 :", mot)
                    final = liste[i % 5] + " " + final
                else:
                    pass
        return final