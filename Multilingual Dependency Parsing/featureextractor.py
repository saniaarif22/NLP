from nltk.compat import python_2_unicode_compatible

printed = False

@python_2_unicode_compatible
class FeatureExtractor(object):
    @staticmethod
    def _check_informative(feat, underscore_is_informative=False):
        """
        Check whether a feature is informative
        """

        if feat is None:
            return False

        if feat == '':
            return False

        if not underscore_is_informative and feat == '_':
            return False

        return True

    @staticmethod
    def find_left_right_dependencies(idx, arcs):
        left_most = 1000000
        right_most = -1
        dep_left_most = ''
        dep_right_most = ''
        for (wi, r, wj) in arcs:
            if wi == idx:
                if (wj > wi) and (wj > right_most):
                    right_most = wj
                    dep_right_most = r
                if (wj < wi) and (wj < left_most):
                    left_most = wj
                    dep_left_most = r
        return dep_left_most, dep_right_most

    @staticmethod
    def extract_features(tokens, buffer, stack, arcs):
        """
        This function returns a list of string features for the classifier

        :param tokens: nodes in the dependency graph
        :param stack: partially processed words
        :param buffer: remaining input words
        :param arcs: partially built dependency tree

        :return: list(str)
        """

        """
        Think of some of your own features here! Some standard features are
        described in Table 3.2 on page 31 of Dependency Parsing by Kubler,
        McDonald, and Nivre

        [http://books.google.com/books/about/Dependency_Parsing.html?id=k3iiup7HB9UC]
        """

        result = []


        global printed
        if not printed:
            #print("This is not a very good feature extractor!")
            printed = True

        # an example set of features:
        if stack:
	    # 1. STK[0]: FORM, LEMMA, POSTAG, FEATS
            stack_idx0 = stack[-1]
            token = tokens[stack_idx0]
            if FeatureExtractor._check_informative(token['word'], True):
                result.append('STK_0_FORM_' + token['word'])

	    if FeatureExtractor._check_informative(token['lemma']):
                result.append('STK_0_LEMMA_' + token['lemma'])

            if FeatureExtractor._check_informative(token['tag']):
                result.append('STK_0_TAG_' + token['tag'])

            if 'feats' in token and FeatureExtractor._check_informative(token['feats']):
                feats = token['feats'].split("|")
                for feat in feats:
                    result.append('STK_0_FEATS_' + feat)

	    # 2. STK[1]: POSTAG -> Reduced accuracy thus removed
            #if len(stack) >= 2:
            #    stack_idx1 = stack[-2]
            #    token = tokens[stack_idx1]
            #    if FeatureExtractor._check_informative(token['tag']):
            #        result.append('STK_1_TAG_' + token['tag'])


            # 3. Left most, right most dependency of stack[0] (already implemented)
            dep_left_most, dep_right_most = FeatureExtractor.find_left_right_dependencies(stack_idx0, arcs)

            if FeatureExtractor._check_informative(dep_left_most):
                result.append('STK_0_LDEP_' + dep_left_most)
            if FeatureExtractor._check_informative(dep_right_most):
                result.append('STK_0_RDEP_' + dep_right_most) 

	    # 4. STK[0]: Number of left children and right children
            lch = 0
            rch = 0
            stack_idx0 = stack[-1]
            for rel in arcs:
                if tokens[rel[0]] == stack_idx0:
                    if tokens[rel[2]]['address'] <= stack_idx0['address']:
                        lch = lch + 1
                    else:
                        rch = rch + 1

            result.append('STK_0_LCHILD_' + str(lch))
            result.append('STK_0_RCHILD_' + str(rch))

	if buffer:
	    # 5. BUF[0]: FORM, LEMMA, POSTAG, FEATS
            buffer_idx0 = buffer[0]
            token = tokens[buffer_idx0]
            if FeatureExtractor._check_informative(token['word'], True):
                result.append('BUF_0_FORM_' + token['word'])

	    if FeatureExtractor._check_informative(token['lemma']):
                result.append('BUF_0_LEMMA_' + token['lemma'])

            if FeatureExtractor._check_informative(token['tag']):
                result.append('BUF_0_TAG_' + token['tag'])

            if 'feats' in token and FeatureExtractor._check_informative(token['feats']):
                feats = token['feats'].split("|")
                for feat in feats:
                    result.append('BUF_0_FEATS_' + feat)

	    # 6. BUF[1]: FORM, POSTAG
            if len(buffer) >= 2:
                buffer_idx1 = buffer[1]
                token = tokens[buffer_idx1]
                if FeatureExtractor._check_informative(token['word'], True):
                    result.append('BUF_1_FORM_' + token['word'])

                if FeatureExtractor._check_informative(token['tag']):
                    result.append('BUF_1_TAG_' + token['tag'])
	
	    # 7. BUF[2]: POSTAG
	    if len(buffer) >= 3:
                buffer_idx2 = buffer[2]
                token = tokens[buffer_idx2]
                if FeatureExtractor._check_informative(token['tag'], True):
                    result.append('BUF_2_FORM_' + token['tag'])

	    # 8. BUF[3]: POSTAG -> Reduced accuracy thus removed
            #if len(buffer) >= 4:
            #    buffer_idx3 = buffer[3]
            #    token = tokens[buffer_idx3]
            #    if FeatureExtractor._check_informative(token['tag'], True):
            #        result.append('BUF_3_FORM_' + token['tag'])

	    # 9. leftmost, rightmost dependency of buffer[0] (already implemented)
            dep_left_most, dep_right_most = FeatureExtractor.find_left_right_dependencies(buffer_idx0, arcs)

            if FeatureExtractor._check_informative(dep_left_most):
                result.append('BUF_0_LDEP_' + dep_left_most)
            if FeatureExtractor._check_informative(dep_right_most):
                result.append('BUF_0_RDEP_' + dep_right_most)

	    # 10. BUF[0]: Number of left children and right children
            #lch = 0
            #rch = 0
            #buffer_idx0 = buffer[0]
            #for rel in arcs:
            #    if tokens[rel[0]] == buffer_idx0:
            #        if tokens[rel[2]]['address'] <= buffer_idx0['address']:
            #            lch = lch + 1
            #        else:
            #            rch = rch + 1

            #result.append('BUF_0_LCHILD_' + str(lch))
            #result.append('BUF_0_RCHILD_' + str(rch))

            if stack and buffer:
            	# 11. Calculate distance between STK[0] and BUF[0]
            	stack_idx0 = stack[-1]
            	stoken = tokens[stack_idx0]
            
            	buffer_idx0 = buffer[0]
            	btoken = tokens[buffer_idx0]

            	result.append('STK_0_BUF_0_DISTANCE_' + str(abs(stack_idx0 - buffer_idx0)))

            	# 12. Count number of verbs between STK[0] and BUF[0]
            	count = 0
            	for v in xrange(stack_idx0, buffer_idx0):
                	if tokens[v]['ctag'] == 'VERB':
                    		count = count + 1

            	result.append('STK_0_BUF_0_VERBS_' + str(count))

        return result
