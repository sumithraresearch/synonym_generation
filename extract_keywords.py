# coding: utf-8
import gensim
import pandas as pd
import logging
logging.basicConfig(format='%(asctime)s : %(levelname)s : %(message)s', level=logging.INFO)



#keywords = pd.read_csv('/Users/sumithra/DSV/BLULab/NLP_Service_Line/Psychiatry/docsConText_KnowledgeBase_targets.txt', header=0, delimiter='\t')
keywords = pd.read_csv('/Users/sumithra/DSV/BLULab/NLP_Service_Line/Psychiatry/prn_targets.txt', header=0, delimiter='\t')
#keywords = pd.read_csv('/Users/sumithra/DSV/BLULab/NLP_Service_Line/Psychiatry/docsConText_KnowledgeBase_modifiers.txt', header=0, delimiter='\t')
keywords = pd.read_csv('/Users/sumithra/DSV/MeDESTO/mimic_experiments/symptom_names_medesto.txt')

#models:

#models = ['mimic_model_non_alpha_size100', 'mimic_model_non_alpha_size400', 'mimic_model_non_alpha_bigram_size100', 'mimic_model_non_alpha_bigram_size400']
models = ['mimic_model_non_alpha_bigram_size800']


#outf = open('prn_most_similar_targets_only_terms_similarity_above_0_6_tmp.txt', 'w')
outf = open('bigram_s800_medesto_most_similar_targets_only_terms_similarity_above_0_3_tmp.txt', 'w')
#outf = open('phrase_most_similar_modifiers.txt', 'w')

related_terms = {}

for m in models:

	model = gensim.models.word2vec.Word2Vec.load(m)
	## look up related terms in model, save in dict
	counter = 0
	#for i in keywords['literal']:
	for i in keywords['symptom']:
		hits_counter = 0
		#k_category = keywords.iloc[counter]['category']
		k_category = 'symptom'
		counter+=1
		try:

			i = i.lower().strip()
			most_similar = model.most_similar(i, topn=2000000000000000)
			for s in most_similar:
				#print s[1]
				if s[1]>=0.6:
					hits_counter+=1
					#print "THRESHOLD "+i
					#print s[0]+'\t'+str(s[1])
					related_term = s[0].strip()
					#print related_term
					## save which models have a related term for a given category and keyword in the original file
					if k_category in related_terms:
						if i in related_terms[k_category]:
							if related_term in related_terms[k_category][i]: 
								in_models = related_terms[k_category][i][related_term]
							#print in_models
								in_models.append(m)
								related_terms[k_category][i][related_term] = in_models
							else:
								related_terms[k_category][i][related_term] = [m]
						else:
							related_terms[k_category][i] = {related_term:[]}
					else:
						related_terms[k_category] = {i:{related_term:[]}}
			print("Number of synonyms for: "+i+" is: "+str(hits_counter))

		except KeyError:
			print(i+" not in vocabulary or multiword phrase")

#print results to file
for k_category in related_terms:
	outf.write("****CATEGORY: "+k_category+"****\n")
	for keyword in related_terms[k_category]:
	#	print "*******"+r+"*******"
		#print keywords.iloc[keyword]
		outf.write('===KEYWORD: '+keyword+"===\n")
		for related_term in related_terms[k_category][keyword]:
#			print related_term
			outf.write(''+related_term+'\n')
#			print related_terms[keyword][related_term]
			#outf.write('\t'+str(related_terms[k_category][keyword][related_term])+'\n')
outf.close()


