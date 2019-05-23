class Faces:

    def __init__(self):
        self.dif_factor = 0.2
        self.faces_found = 0
        self.faces_locations = []

    def verify_face(self, new_face):
        matches = False
        for old_face in self.faces_locations:
            (nfx, nfy, nfw, nfh) = new_face
            (ofx, ofy, ofw, ofh) = old_face
            cfx = abs(nfx-ofx)
            cfy = abs(nfy-ofy)
            cfw = abs(nfw-ofw)
            cfh = abs(nfh-ofh)
            w_factor = ofw * self.dif_factor
            h_factor = ofh * self.dif_factor
            if cfx < w_factor and cfy < h_factor and cfw < w_factor and cfh < h_factor:
                matches = True
                self.faces_locations.remove(old_face)
                self.faces_locations.append(new_face)
                return
        self.faces_locations.append(new_face)
        self.faces_found += 1

    def get_faces_count(self):
        return self.faces_found