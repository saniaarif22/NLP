class Transition(object):
    """
    This class defines a set of transitions which are applied to a
    configuration to get the next configuration.
    """
    # Define set of transitions
    LEFT_ARC = 'LEFTARC'
    RIGHT_ARC = 'RIGHTARC'
    SHIFT = 'SHIFT'
    REDUCE = 'REDUCE'

    def __init__(self):
        raise ValueError('Do not construct this object!')

    @staticmethod
    def left_arc(conf, relation):
        """
            :param configuration: is the current configuration
            :return : A new configuration or -1 if the pre-condition is not satisfied
        """
	#print "in left arc"
	if not conf.buffer or not conf.stack:
            # either buffer or stack not present
            return -1

	# check if stack has more content than root
        if len(conf.stack) == 1:
            return -1
	
	stacktop = conf.stack[-1]
	
	#precondition
	for rel in conf.arcs:
		if stacktop == rel[2]:
			return -1
	
	#remove from stack
	st = conf.stack.pop()
	bf = conf.buffer[0]

	#add to arcs
	conf.arcs.append((bf,relation,st))
	
        #raise NotImplementedError('Please implement left_arc!')
        #return -1

    @staticmethod
    def right_arc(conf, relation):
        """
            :param configuration: is the current configuration
            :return : A new configuration or -1 if the pre-condition is not satisfied
        """
	#print "in right arc"
	
	#print conf
	#print relation

        if not conf.buffer or not conf.stack:
	    # either buffer or stack not present
            return -1

        # You get this one for free! Use it as an example.

        idx_wi = conf.stack[-1]
        idx_wj = conf.buffer.pop(0)

        conf.stack.append(idx_wj)
        conf.arcs.append((idx_wi, relation, idx_wj))

    @staticmethod
    def reduce(conf):
        """
            :param configuration: is the current configuration
            :return : A new configuration or -1 if the pre-condition is not satisfied
        """
	#print "in reduce"
	if not conf.stack:
            # stack not present
            return -1
	
	st = conf.stack[-1]
	flag = False
	for rel in conf.arcs:
		if st == rel[2]:
			flag=True
			break
	
	if not flag:
		return -1

	conf.stack.pop()
        #raise NotImplementedError('Please implement reduce!')
        

    @staticmethod
    def shift(conf):
        """
            :param configuration: is the current configuration
            :return : A new configuration or -1 if the pre-condition is not satisfied
        """
	#print "in shift"
	if not conf.buffer:
            # buffer not present
            return -1
	
	bf = conf.buffer.pop(0)
	conf.stack.append(bf)
	
        #raise NotImplementedError('Please implement shift!')
        #return -1
