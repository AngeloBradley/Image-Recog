

def gather_images_for_gui(search_results):
    image_data_b64 = []
    # iterate over search_results and load images
    for result in search_results:
        # print(result)
        with open(cache_location + result) as r:
            image_data_b64.append(r.read())

    # print(image_data_b64)
    return image_data_b64

def search(query):
    '''
        this code assumes that the query has gone through some sort of security check and 
        that the query is made up only of words separated by spaces. Will add validation 
        features if necessary.
    '''
    # -------------------------------------------------------------------------------------
    '''
        an "and" or "&" function could be implemented. It could work something like this:
        
        left_term and right_term

        -- grab the lists from both caption.txt files (left_term.txt and right_term.txt)
        -- iterate over one list, image by image, storing the image in some variable like
        and_list if the image is also present in the other list. The tricky part would be 
        sorting the list. By default, the method above would give confidence level
        preference to the left term. What this means is:

        the query "dog and fire hydrant" would result in a list where the images are more
        likely to actually contain a dog. The possibility of any image actually containing a 
        fire hydrant would be hit or miss.

        you could sort by both but that probably wouldn't improve the results much because the 
        confidence levels vary so wildly.
    '''
    # -------------------------------------------------------------------------------------

    search_terms = query.split(' ')
    search_results = []
    seen = set()

    for term in search_terms:
        # attempt to pass term to dictionary
        # if the dictionary throws a keyerror, return nothing
        # if the dictionary returns a value, store as valid_term

        try:
            valid_terms = dictionary[term]
            # print(valid_terms)

            for v_term in valid_terms:

                with open(caption_pool_location + v_term + '.txt') as caption_dot_text:
                    images = caption_dot_text.readlines()
                    # image format -> "uuid.txt confidence"
                    for image in images:
                        # split image data into uuid and confidence
                        i = image.split(' ')
                        if i[0] in seen:
                            pass
                        else:
                            seen.add(i[0])
                            search_results.append(i[0])

        except KeyError:
            # search term was not in dictionary, continue with the for loop
            continue
    # print(search_results)
    return gather_images_for_gui(search_results)
