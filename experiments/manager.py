import os
import glob

class Env(object):
    def __init__(self,root_dir:str, dep_links:dict):
        self.root_dir=root_dir
        self.dep_links=dep_links

        #reset dependence links
        print('reset dep links')
        self.unset_dep_links()
        self.set_dep_links()


    def set_dep_links(self):
        for k in self.dep_links:
            src_path = os.path.join(self.root_dir, k)
            des_path = os.path.join(self.root_dir, self.dep_links[k])
            command = 'ln -s %s %s' %(des_path, src_path)
            os.system(command)
            # print('run: ',command)


    def unset_dep_links(self):
        for k in self.dep_links:
            path = os.path.join(self.root_dir, k)
            command = 'unlink %s' %(path)
            if os.path.islink(path):
                state = os.system(command)
                # print('run: ',command)


class Experimet(Env):
    def __init__(self, dir, dep_links):
        Env.__init__(self, dir, dep_links=dep_links)
        self.tag = os.path.basename(dir)
        self.dir = dir


    def run(self):
        command = 'cd %s && python task.py -n %s' % (self.dir,self.tag)
        print('run: %s' % (command))
        os.system(command)


class Manager(Env):
    def __init__(self, root_dir=os.path.abspath('./')):
        links={
            'log':'../log',
            'checkpoint': '../checkpoint',
            'data': '../data',
        }
        Env.__init__(self, root_dir=root_dir, dep_links=links)


    def scan(self):
        dirs = glob.glob(os.path.join(self.root_dir,'exp_*'))
        dirs.sort()

        dep_links={
            'net':os.path.join(self.root_dir,'..','src','net'),
            'didi_data': os.path.join(self.root_dir, '..', 'src', 'didi_data'),
            'kitti_data': os.path.join(self.root_dir, '..', 'src', 'kitti_data'),
            'tracklets': os.path.join(self.root_dir, '..', 'src', 'tracklets'),
            'data.py': os.path.join(self.root_dir, '..', 'src', 'data.py'),
            'utils': os.path.join(self.root_dir, '..', 'src', 'utils'),
            'train.py': os.path.join(self.root_dir, '..', 'src', 'train.py'),
            'tracking.py': os.path.join(self.root_dir, '..', 'src', 'tracking.py'),
            'task.py': os.path.join(self.root_dir, '..', 'src', 'task.py'),
        }
        return [Experimet(dir=dir,dep_links=dep_links) for dir in dirs]

    def summary(self, exps):
        print('\n------------------------------------------------------------------------------')
        print('\nexperiments has :')
        for i, exp in enumerate(exps):
            print('    %d: %s' % (i, exp.tag))

if __name__ == '__main__':
    man = Manager()
    print('\n\n start scan all experiments')
    exps = man.scan()

    man.summary(exps)
    for i,exp in enumerate(exps):
        exp.run()