"""Atom indexes between two similar ASE atoms objects may be inconsistent. This
module lets you keeps track of individual atoms between two similar ASE atoms objects.
"""
#!/usr/bin/env python
from math import sqrt
from numpy import isclose

def find_ads_slab_pairs(slab, ads, difference_tol=0.3):
    """
    Matches and pairs indices of atoms in `ads` with atoms in `slab` using atomic
    distances in unit cell.

    This function only works with atoms objects from ASE. Use of this function is
    not limited to catalyst models. User may use any two atoms objects in place
    of `ads` and `slab` so long as they follow:

    -The number of atoms in `ads` >= the number of atoms in `slab`
    -The atoms being paired have coordinates that match within the the value set
    with `difference_tol`.

    Parameters
    ----------
    slab : An atoms object from ASE. (ie. A slab model of a catalyst surface.)

    ads : An atoms object from ASE. (ie. A slab model of a catalyst surface with
        an adsorbed molecule.)

    difference_tol (default: 0.3) : Tolerance used when comparing atomic distances.

    Returns
    -------
    pair : A list of lists. Each nested list contains a pair of indexes for the two
        matching atoms as such:
        `[slab_atom_index,ads_atom_index]`
    """

    slab_positions = []

    for s_loc in slab:

        #Calculating the distance of each atom in slab from reference points
        distance_0 = sqrt(s_loc.position[0]**2 + s_loc.position[1]**2 +
                          (s_loc.position[2])**2)

        distance_1 = sqrt((s_loc.position[0]-10)**2 + (s_loc.position[1]-10)**2 +
                          (s_loc.position[2])**2)

        distance_2 = sqrt((s_loc.position[0]-0)**2 + (s_loc.position[1]-10)**2 +
                          (s_loc.position[2])**2)

        distance_3 = sqrt((s_loc.position[0]-10)**2 + (s_loc.position[1]-0)**2 +
                          (s_loc.position[2])**2)

        #List of slab atom index and distances
        slab_positions.append([s_loc.index, distance_0, distance_1, distance_2, distance_3])

    ads_positions = []

    for a_loc in ads:

        #Calculating the distance of each atom in ads from reference points
        distance_0 = sqrt(a_loc.position[0]**2 + a_loc.position[1]**2 +
                          (a_loc.position[2])**2)

        distance_1 = sqrt((a_loc.position[0]-10)**2 + (a_loc.position[1]-10)**2 +
                          (a_loc.position[2])**2)

        distance_2 = sqrt((a_loc.position[0]-0)**2 + (a_loc.position[1]-10)**2 +
                          (a_loc.position[2])**2)

        distance_3 = sqrt((a_loc.position[0]-10)**2 + (a_loc.position[1]-0)**2 +
                          (a_loc.position[2])**2)

        #List of ads atom index and distances
        ads_positions.append([a_loc.index, distance_0, distance_1, distance_2, distance_3])

    pair = []

    for s_loc in slab_positions:

        mult = []

        for a_loc in ads_positions:

            if (abs(s_loc[1]-a_loc[1]) <= difference_tol and
                    abs(s_loc[2]-a_loc[2]) <= difference_tol and
                    abs(s_loc[3]-a_loc[3]) <= difference_tol and
                    abs(s_loc[4]-a_loc[4]) <= difference_tol):

                #List of matching atom index in ads with two differences in distance
                mult.append([a_loc[0], (s_loc[1]-a_loc[1]), s_loc[2]-a_loc[2]])

        #Placeholder in mult if no matches are found
        if not mult:
            mult.append(['n'])

        #List of index pairs found (slab, ads)
        pair.append([s_loc[0], mult[0][0]])

    return pair

def find_symmetric_pairs(slab, atom_index_set_1, atom_index_set_2):
    """
    Finds pairs of atoms in slab that are symmetric with each other about the center of mass. This
    function returns pairs of indexes to the two atoms that are symmetric. Two lists must be supplied.
    The first contains the indexes of the atoms above the symmetry plane. The second contains the 
    indexes of the atoms below the symmetry plane.

    Parameters
    ----------
    slab : An atoms object from ASE.

    atom_index_set_1 : List of atom indexes in slab on one side of the plane of symmetry.

    atom_index_set_2 : List of atom indexes in slab on the other side of the plane of symmetry.

    Returns
    -------
    symmetric_atom_index_pairs : A list of lists. Each nested list contains a pair of indexes for
    the two symmetric atoms.
    """

    center_of_mass = slab.get_center_of_mass()

    distances_1 = {}

    distances_2 = {}

    symmetric_atom_index_pairs = []

    for dex in atom_index_set_1:

            distances_1[dex] = [slab[dex].position[0] - center_of_mass[0],
                                slab[dex].position[1] - center_of_mass[1],
                                slab[dex].position[2] - center_of_mass[2]]

    for dex in atom_index_set_2:

            distances_2[dex] = [slab[dex].position[0] - center_of_mass[0],
                                slab[dex].position[1] - center_of_mass[1],
                                slab[dex].position[2] - center_of_mass[2]]

    for first_dex, first_distance in distances_1.items():

            for second_dex, second_distance in distances_2.items():

                if (isclose([first_distance[0]],[second_distance[0] * -1]) and
                    isclose([first_distance[1]],[second_distance[1] * -1]) and
                    isclose([first_distance[2]],[second_distance[2] * -1])):

                    symmetric_atom_index_pairs.append([first_dex, second_dex])

    return symmetric_atom_index_pairs