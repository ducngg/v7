class Alphabet():
    ALL = 'abcdefghijklmnopqrstuvwxyz'
    LATIN = [letter for letter in ALL]
    CONSONANTS = ['b', 'c', 'd', 'f', 'g', 'h', 'j', 'k', 'l', 'm', 'n', 'p', 'q', 'r', 's', 't', 'v', 'w', 'x', 'y', 'z']
    VOWELS = ['a', 'e', 'i', 'o', 'u']
    VOWELS_Y = ['a', 'e', 'i', 'o', 'u', 'y']

class Vietnamese(Alphabet):
    """
    Controversial very rare words like `Đắk Lắk, Kạn, Kon, ...`
    """
    tones = [0, 1, 2, 3, 4, 5, 6, 7]
    
    # Treat `i` and `y` the same so there will be no `y`; treat `p`, `t`, `c`, `ch`  and  `m`, `n`, `ng`, `nh` the same
    rhymes_families = [
        'a',
        'an',
        'anh',
        'ang',
        'am',
        'ăn',
        'ăng',
        'ăm',
        'ân',
        'âng',
        'âm',
        'e',
        'en',
        'eng',
        'em',
        'ê',
        'ên',
        'ênh',
        'êm',
        'i',
        'in',
        'inh',
        'im',
        'o',
        'on',
        'ong',
        'om',
        'ô',
        'ôn',
        'ông',
        'ôm',
        'ơ',
        'ơn',
        'ơm',
        'u',
        'un',
        'ung',
        'um',
        'ư',
        'ưn',
        'ưng',
        'ưm',
        'ai',
        'ay',
        'ây',
        'oi',
        'ôi',
        'ơi',
        'ui',
        'ưi',
        'oa',
        'oan',
        'oanh',
        'oang',
        'oam',
        'oăn',
        'oăng',
        'oăm',
        'uân',
        'uâng',
        'oe',
        'oen',
        'uê',
        'uên',
        'uênh', #
        'uy',
        'uyn',
        'uynh',
        'uym',
        'ua',
        'uôn',
        'uông',
        'uôm',
        'uơ',
        'uơn',
        'ia',
        'iên',
        'iêng',
        'iêm',
        'ưa',
        'ươn',
        'ương',
        'ươm',
        'ao',
        'au',
        'âu',
        'eo',
        'êu',
        'iu',
        'ưu',
        'iêu',
        'ươu',
        'oai',
        'oay',
        'uây',
        'uôi',
        'uơi',
        'ươi',
        'uya',
        'uyên',
        'oao',
        'oau',
        'oeo',
        'uyu',
        'oong',
    ]
    # Rhymes like `iên` and `iêu` will be `yên` and `yêu`
    rhymes_families_isolated = [
        'a',
        'an',
        'anh',
        'ang',
        'am',
        'ăn',
        'ăng',
        'ăm',
        'ân',
        'âng',
        'âm',
        'e',
        'en',
        'eng',
        'em',
        'ê',
        'ên',
        'ênh',
        'êm',
        'i',
        'in',
        'inh',
        'im',
        'o',
        'on',
        'ong',
        'om',
        'ô',
        'ôn',
        'ông',
        'ôm',
        'ơ',
        'ơn',
        'ơm',
        'u',
        'un',
        'ung',
        'um',
        'ư',
        'ưn',
        'ưng',
        'ưm',
        'y',
        'ai',
        'ay',
        'ây',
        'oi',
        'ôi',
        'ơi',
        'ui',
        'ưi',
        'oa',
        'oan',
        'oanh',
        'oang',
        'oam',
        'oăn',
        'oăng',
        'oăm',
        'uân',
        'uâng',
        'oe',
        'oen',
        'uê',
        'uên',
        'uênh', #
        'uy',
        'uyn',
        'uynh',
        'uym',
        'ua',
        'uôn',
        'uông',
        'uôm',
        'uơ',
        'uơn',
        'ia',
        'yên',
        'yêng',
        'yêm',
        'ưa',
        'ươn',
        'ương',
        'ươm',
        'ao',
        'au',
        'âu',
        'eo',
        'êu',
        'iu',
        'ưu',
        'yêu',
        'ươu',
        'oai',
        'oay',
        'uây',
        'uôi',
        'uơi',
        'ươi',
        'uya',
        'uyên',
        'oao',
        'oau',
        'oeo',
        'uyu',
        'oong',
    ]
    # Base for other rhymes_families lists
    rhymes_families_with_other_consonants = [
        'a',
        'an',
        'anh',
        'ang',
        'am',
        'ăn',
        'ăng',
        'ăm',
        'ân',
        'âng',
        'âm',
        'e',
        'en',
        'eng',
        'em',
        'ê',
        'ên',
        'ênh',
        'êm',
        'i',
        'in',
        'inh',
        'im',
        'o',
        'on',
        'ong',
        'om',
        'ô',
        'ôn',
        'ông',
        'ôm',
        'ơ',
        'ơn',
        'ơm',
        'u',
        'un',
        'ung',
        'um',
        'ư',
        'ưn',
        'ưng',
        'ưm',
        'y',
        'ai',
        'ay',
        'ây',
        'oi',
        'ôi',
        'ơi',
        'ui',
        'ưi',
        'oa',
        'oan',
        'oanh',
        'oang',
        'oam',
        'oăn',
        'oăng',
        'oăm',
        'uân',
        'uâng',
        'oe',
        'oen',
        'uê',
        'uên',
        'uênh', #
        'uy',
        'uyn',
        'uynh',
        'uym',
        'ua',
        'uôn',
        'uông',
        'uôm',
        'uơ',
        'uơn',
        'ia',
        'iên',
        'iêng',
        'iêm',
        'ưa',
        'ươn',
        'ương',
        'ươm',
        'ao',
        'au',
        'âu',
        'eo',
        'êu',
        'iu',
        'ưu',
        'iêu',
        'ươu',
        'oai',
        'oay',
        'uây',
        'uôi',
        'uơi',
        'ươi',
        'uya',
        'uyên',
        'oao',
        'oau',
        'oeo',
        'uyu',
        'oong',
    ]
    # Limited rhyme can go with `z`, handle special cases
    rhymes_families_with_gi = [
        'a',
        'an',
        'anh',
        'ang',
        'am',
        'ăn',
        'ăng',
        'ăm',
        'ân',
        'âng',
        'âm',
        'e',
        'en',
        'eng',
        'em',
        'ê',
        'ên', # Special iên
        'ênh',
        'êng', # Special iêng
        'êm',
        '', # Special i
        'n', # Special in
        'o',
        'on',
        'ong',
        'om',
        'ô',
        'ôn',
        'ông',
        'ôm',
        'ơ',
        'ơn',
        'ơm',
        'u',
        'un',
        'ung',
        'um',
        'ư',
        'ưn',
        'ưng',
        'ưm',
        'ai',
        'ay',
        'ây',
        'oi',
        'ôi',
        'ơi',
        'ui', #
        'ưi', #
        'ua', #
        'uông', #
        'ưa',
        'ươn',
        'ương',
        'ươm',
        'ao',
        'au',
        'âu',
        'eo',
        'êu',
        'ưu', #
        'ươu', #
        'uôi', #
        'ươi', #
        'oong',
    ]
    # Limited rhyme can go with `ng`, handle special cases
    rhymes_families_with_ng = [
        'a',
        'an',
        'anh',
        'ang',
        'am',
        'ăn',
        'ăng',
        'ăm',
        'ân',
        'âng',
        'âm',
        'o',
        'on',
        'ong',
        'om',
        'ô',
        'ôn',
        'ông',
        'ôm',
        'ơ',
        'ơn',
        'ơm',
        'u',
        'un',
        'ung',
        'um',
        'ư',
        'ưn',
        'ưng',
        'ưm',
        'ai',
        'ay',
        'ây',
        'oi',
        'ôi',
        'ơi',
        'ui',
        'ưi',
        'oa',
        'oan',
        'oanh',
        'oang',
        'oam',
        'oăn',
        'oăng',
        'oăm',
        'uân',
        'uâng',
        'oe',
        'oen',
        'uê',
        'uên',
        'uênh', #
        'uy',
        'uyn',
        'uynh',
        'uym',
        'ua',
        'uôn',
        'uông',
        'uôm',
        'uơ',
        'uơn',
        'ưa',
        'ươn',
        'ương',
        'ươm',
        'ao',
        'au',
        'âu',
        'ưu',
        'ươu',
        'oai',
        'oay',
        'uây',
        'uôi',
        'uơi',
        'ươi',
        'uya',
        'uyên',
        'oao',
        'oau',
        'oeo',
        'uyu',
        'oong',
    ]
    # Limited rhyme can go with `g`, handle special cases
    rhymes_families_with_g = [
        'a',
        'an',
        'anh',
        'ang',
        'am',
        'ăn',
        'ăng',
        'ăm',
        'ân',
        'âng',
        'âm',
        'o',
        'on',
        'ong',
        'om',
        'ô',
        'ôn',
        'ông',
        'ôm',
        'ơ',
        'ơn',
        'ơm',
        'u',
        'un',
        'ung',
        'um',
        'ư',
        'ưn',
        'ưng',
        'ưm',
        'ai',
        'ay',
        'ây',
        'oi',
        'ôi',
        'ơi',
        'ui',
        'ưi',
        'oa',
        'oan',
        'oanh',
        'oang',
        'oam',
        'oăn',
        'oăng',
        'oăm',
        'uân',
        'uâng',
        'oe',
        'oen',
        'uê',
        'uên',
        'uênh', #
        'uy',
        'uyn',
        'uynh',
        'uym',
        'ua',
        'uôn',
        'uông',
        'uôm',
        'uơ',
        'uơn',
        'ưa',
        'ươn',
        'ương',
        'ươm',
        'ao',
        'au',
        'âu',
        'ưu',
        'ươu',
        'oai',
        'oay',
        'uây',
        'uôi',
        'uơi',
        'ươi',
        'uya',
        'uyên',
        'oao',
        'oau',
        'oeo',
        'uyu',
        'oong',
    ]
    # Limited rhyme can go with `ngh` or `gh`.
    rhymes_families_with_ngh_gh = [
        'e',
        'en',
        'eng',
        'em',
        'ê',
        'ên',
        'ênh',
        'êm',
        'i',
        'in',
        'inh',
        'im',
        'ia',
        'iên',
        'iêng',
        'iêm',
        'eo',
        'êu',
        'iu',
        'iêu',
    ]
    # rhymes_families_with_q_start_with_o = ['oa', 'oan', 'oanh', 'oang', 'oam', 'oăn', 'oăng', 'oăm', 'oe', 'oen', 'oai', 'oay', 'oao', 'oau', 'oeo']
    rhymes_families_with_q = [
        'ua',
        'uan',
        'uanh',
        'uang',
        'uam',
        'uăn',
        'uăng',
        'uăm',
        'uân',
        'uâng',
        'ue',
        'uen',
        'uê',
        'uên',
        'uênh', #
        'uy', 'ui', #
        'uyn', 'uin', #
        'uynh',
        'uym',
        'uông', # Special: quốc
        'uơ',
        'uơn', # Special: quớt
        'uai',
        'uay',
        'uây',
        'uơi', # Special: quới
        'uya', #
        'uyên', 
        'uao',
        'uau',
        'ueo',
        'uyu', #
    ]
    # Limited rhyme can go with `k`
    rhymes_families_with_k = [
        'e',
        'en',
        'eng',
        'em',
        'ê',
        'ên',
        'ênh',
        'êm',
        'i',
        'in',
        'inh',
        'im',
        'y',
        'ia',
        'iên',
        'iêng',
        'iêm',
        'eo',
        'êu',
        'iu',
        'iêu',
    ]
    # Limited rhyme can go with `c`
    rhymes_families_with_c = [
        'a',
        'an',
        'anh',
        'ang',
        'am',
        'ăn',
        'ăng',
        'ăm',
        'ân',
        'âng',
        'âm',
        'o',
        'on',
        'ong',
        'om',
        'ô',
        'ôn',
        'ông',
        'ôm',
        'ơ',
        'ơn',
        'ơm',
        'u',
        'un',
        'ung',
        'um',
        'ư',
        'ưn',
        'ưng',
        'ưm',
        'ai',
        'ay',
        'ây',
        'oi',
        'ôi',
        'ơi',
        'ui',
        'ưi',
        'ua',
        'uôn',
        'uông',
        'uôm',
        'ưa',
        'ươn',
        'ương',
        'ươm',
        'ao',
        'au',
        'âu',
        'ưu',
        'ươu',
        'uôi',
        'ươi',
        'oong',
    ]
    
    # All consonants in Vietnamese writing
    consonants = [
        'b', 
        'c', 'ch', 
        'd', 'đ', 
        'g', 'gh', 'gi', 
        'h', 
        'k', 'kh', 
        'l', 
        'm', 
        'n', 'ng', 'nh', 'ngh',
        'p', 'ph', 
        'q', 
        'r', 
        's', 
        't', 'th', 'tr',
        'v', 
        'x', 
    ]
    # Regular consonants (can go directly with `rhymes_families_with_other_consonants`)
    other_consonants = [
        'b', 
        'ch', 
        'd', 'đ', 
        
        'h', 
        'kh', 
        'l', 
        'm', 
        'n', 'nh',
        'p', 'ph', 
        
        'r', 
        's', 
        't', 'th', 'tr',
        'v', 
        'x', 
    ]
    # Grouped similar consonants to a family
    consonant_families = [
        '0',
        'b', 
        'ch', 
        'd', 'đ', 
        'g', 'z', 
        'h', 
        'k', 'kh', 
        'l', 
        'm', 
        'n', 'ng', 'nh',
        'p', 'ph', 
        'r', 
        's', 
        't', 'th', 'tr',
        'v', 
        'x', 
    ]
    
    # Diacritic position on a rhyme
    diacritic_position = {
        'a': 0,
        'an': 0,
        'anh': 0,
        'ang': 0,
        'am': 0,
        'ăn': 0,
        'ăng': 0,
        'ăm': 0,
        'ân': 0,
        'âng': 0,
        'âm': 0,
        'e': 0,
        'en': 0,
        'eng': 0,
        'em': 0,
        'ê': 0,
        'ên': 0,
        'ênh': 0,
        'êm': 0,
        'i': 0,
        'in': 0,
        'inh': 0,
        'im': 0,
        'o': 0,
        'on': 0,
        'ong': 0,
        'om': 0,
        'ô': 0,
        'ôn': 0,
        'ông': 0,
        'ôm': 0,
        'ơ': 0,
        'ơn': 0,
        'ơm': 0,
        'u': 0,
        'un': 0,
        'ung': 0,
        'um': 0,
        'ư': 0,
        'ưn': 0,
        'ưng': 0,
        'ưm': 0,
        'ai': 0,
        'ay': 0,
        'ây': 0,
        'oi': 0,
        'ôi': 0,
        'ơi': 0,
        'ui': 0,
        'ưi': 0,
        'oa': 0, ## q -> 1
        'oan': 1,
        'oanh': 1,
        'oang': 1,
        'oam': 1,
        'oăn': 1,
        'oăng': 1,
        'oăm': 1,
        'uân': 1,
        'uâng': 1,
        'oe': 0,
        'oen': 1,
        'uê': 1,
        'uên': 1,
        'uênh': 1, 
        'uy': 0, ## q -> 1
        'uyn': 1,
        'uynh': 1,
        'uym': 1,
        'ua': 0,
        'uôn': 1,
        'uông': 1,
        'uôm': 1,
        'uơ': 1,
        'uơn': 1,
        'ia': 0,
        'iên': 1,
        'iêng': 1,
        'iêm': 1,
        'ưa': 0,
        'ươn': 1,
        'ương': 1,
        'ươm': 1,
        'ao': 0,
        'au': 0,
        'âu': 0,
        'eo': 0,
        'êu': 0,
        'iu': 0,
        'ưu': 0,
        'iêu': 1,
        'ươu': 1,
        'oai': 1,
        'oay': 1,
        'uây': 1,
        'uôi': 1,
        'uơi': 1,
        'ươi': 1,
        'uya': 1,
        'uyên': 2,
        'oao': 1,
        'oau': 1,
        'oeo': 1,
        'uyu': 1,
        'oong': 1,
    }
    diacritic_0_chars = ['a', 'ă', 'â', 'e', 'ê', 'i', 'o', 'ô', 'ơ', 'u', 'ư', 'y']
    diacritic_1_chars = ['á', 'ắ', 'ấ', 'é', 'ế', 'í', 'ó', 'ố', 'ớ', 'ú', 'ứ', 'ý']
    diacritic_2_chars = ['à', 'ằ', 'ầ', 'è', 'ề', 'ì', 'ò', 'ồ', 'ờ', 'ù', 'ừ', 'ỳ']
    diacritic_3_chars = ['ả', 'ẳ', 'ẩ', 'ẻ', 'ể', 'ỉ', 'ỏ', 'ổ', 'ở', 'ủ', 'ử', 'ỷ']
    diacritic_4_chars = ['ã', 'ẵ', 'ẫ', 'ẽ', 'ễ', 'ĩ', 'õ', 'ỗ', 'ỡ', 'ũ', 'ữ', 'ỹ']
    diacritic_5_chars = ['ạ', 'ặ', 'ậ', 'ẹ', 'ệ', 'ị', 'ọ', 'ộ', 'ợ', 'ụ', 'ự', 'ỵ']
    
    @staticmethod
    def chars_with_diacritic(char: str) -> list[str]:
        '''
        From a non-diacritic Vietnamese `vowel` to a list of 6 characters of that vowel with diacritics.
        '''
        if char not in Vietnamese.diacritic_0_chars:
            return None
        char_index = Vietnamese.diacritic_0_chars.index(char)
        return [
            char,
            Vietnamese.diacritic_1_chars[char_index],
            Vietnamese.diacritic_2_chars[char_index],
            Vietnamese.diacritic_3_chars[char_index],
            Vietnamese.diacritic_4_chars[char_index],
            Vietnamese.diacritic_5_chars[char_index],
        ]
        
    i_s = ['i', 'í', 'ì', 'ỉ', 'ĩ', 'ị']
    y_s = ['y', 'ý', 'ỳ', 'ỷ', 'ỹ', 'ỵ']
    a_s = []
    aw_s = []
    aa_s = []
    # ... add later if necessary
    
    def rhyme_with_tones(rhyme_family: str, consonant_family: str) -> list[str]:
        """
        From a `rhyme_family` to a list of toned rhyme of that family.
        If the rhyme family is enterable (ends with a consonant), the list will contain 8 tones, otherwise 6 tones.
        
        Note: `consonant_family` is neccessary because with `k`, the diacritic position of some rhymes are different.
        """
        if rhyme_family not in Vietnamese.rhymes_families or consonant_family not in Vietnamese.consonant_families:
            return None
        
        # Position of the diacritic sign in a rhyme
        diacritic_index = Vietnamese.diacritic_position[rhyme_family]
        
        # Special case: quá, quý, quẻ instead of óa, úy, ỏe
        if consonant_family == 'k' and rhyme_family in ['oa', 'uy', 'oe']:
            diacritic_index = 1
            
        # Get the list of the vowel with all diacritics
        chars_with_diacritic = Vietnamese.chars_with_diacritic(rhyme_family[diacritic_index])
            
        # Take 6 tones first
        rhyme_6_tones = [
            rhyme_family[:diacritic_index] + toned + rhyme_family[diacritic_index + 1:]
            for toned in chars_with_diacritic
        ]
        
        # 2 `entering` tones
        """
        Enterable rhyme are the rhyme that ends with a consonant.
        Rhyme: *n, *ng, *m, *nh
        Entering form: *t, *c, *p, *ch
        """
        if rhyme_family[-2:] == 'ng':
            entering_tones = [
                rhyme_6_tones[1][:-2] + 'c',
                rhyme_6_tones[5][:-2] + 'c',
            ]
        elif rhyme_family[-2:] == 'nh':
            entering_tones = [
                rhyme_6_tones[1][:-2] + 'ch',
                rhyme_6_tones[5][:-2] + 'ch',
            ]
        elif rhyme_family[-1:] == 'n':
            entering_tones = [
                rhyme_6_tones[1][:-1] + 't',
                rhyme_6_tones[5][:-1] + 't',
            ]
        elif rhyme_family[-1:] == 'm':
            entering_tones = [
                rhyme_6_tones[1][:-1] + 'p',
                rhyme_6_tones[5][:-1] + 'p',
            ]
        else:
            entering_tones = []
        
        final_rhymes = rhyme_6_tones + entering_tones
        
        return final_rhymes
    
    @staticmethod
    def word_with_tones(consonant_family: str, rhyme_family: str) -> list[list[str]]:
        '''
        More general function of synthesize, obtain all tones of a given consonant_family and rhyme_family.
        
        Note: This function returns a list of list due to the non-injective property mentioned in README.md.
        '''
        if rhyme_family not in Vietnamese.rhymes_families or consonant_family not in Vietnamese.consonant_families:
            return None
        
        # Maps from consonant family to actual consonant in Vietnamese writing
        final_consonant = consonant_family
        
        if consonant_family in ['0']:
            final_consonant = ''
        elif consonant_family in ['z']:
            if rhyme_family in ['i', 'in', 'iên', 'iêng']:
                final_consonant = 'g'
            else:
                final_consonant = 'gi'
        elif consonant_family in ['g', 'ng']:
            if rhyme_family in Vietnamese.rhymes_families_with_ngh_gh:
                final_consonant = consonant_family + 'h'
        elif consonant_family in ['k']:
            if rhyme_family in Vietnamese.rhymes_families_with_c:
                final_consonant = 'c'
            elif rhyme_family in Vietnamese.rhymes_families_with_k:
                final_consonant = 'k'
            else:
                final_consonant = 'q'
            
        rhyme_with_tones = Vietnamese.rhyme_with_tones(rhyme_family, consonant_family)
        
        if final_consonant == 'q':
            # All rhyme starts with `o` change to `u` => All rhymes start with `u`
            rhyme_with_tones = ['u' + rhyme_with_tone[1:] for rhyme_with_tone in rhyme_with_tones]
        elif final_consonant == '':
            # All rhymes starts with `iê` change to its isolated form
            if rhyme_family in ['iên', 'iêng', 'iêm', 'iêu']:
                rhyme_with_tones = [Vietnamese.i2y(rhyme_with_tone) for rhyme_with_tone in rhyme_with_tones]
        
        # Cuốc - Quốc case
        if consonant_family == 'k' and rhyme_family == 'uông':
            return [
                [final_consonant + rhyme_with_tone for rhyme_with_tone in rhyme_with_tones],
                ['q' + rhyme_with_tone for rhyme_with_tone in rhyme_with_tones]
            ]
        # If `rhyme_family` is `i`, there are `-i` form and `-y` form
        # Not accept `gy`, `ghy`, `nghy`, ...
        elif consonant_family not in ['z', 'g', 'ng', 'b', 'ch', 'd', 'đ', 'kh', 'p', 'ph', 'r', 'tr', 'x'] and rhyme_family == 'i' :
            return [
                [final_consonant + rhyme_with_tone for rhyme_with_tone in rhyme_with_tones],
                [final_consonant + Vietnamese.i2y(rhyme_with_tone) for rhyme_with_tone in rhyme_with_tones]
            ]
        else:
            return [[final_consonant + rhyme_with_tone for rhyme_with_tone in rhyme_with_tones]] 
    
    @staticmethod
    def synthesize(consonant_family: str, rhyme_family: str, tone: int) -> list[str]:
        """
        Reverse function of `analyze()`.

        Args:
            consonant_family (str): See `Vietnamese.consonant_families`.
            rhyme_family (str): See `Vietnamese.rhymes_families`.
            tone (int): See `Vietnamese.tones`.

        Returns:
            List of the words those are formed by combining the three parameters.
            - ['quyết'] <- synthesize('k', 'uyên', 6)
            - ['gì'] <- synthesize('z', 'i', 2)
            - ['cưỡi'] <- synthesize('k', 'ươi', 4)
            - ['kị', 'kỵ'] <- synthesize('k', 'i', 5)
            - ['cuốc', 'quốc'] <- synthesize('k', 'uông', 6)
            - ['nghiêm'] <- synthesize('ng', 'iêm', 0)
        """
        tone = int(tone)
        if rhyme_family not in Vietnamese.rhymes_families or consonant_family not in Vietnamese.consonant_families or tone not in Vietnamese.tones:
            return []
        else:
            return [word_with_tones[tone] for word_with_tones in Vietnamese.word_with_tones(consonant_family, rhyme_family)]
    
    @staticmethod
    def y2i(rhyme: str):
        """
        Change the initial `y` to `i`, example:
        - yên -> iên
        - ỹ -> ĩ
        - yếm -> iếm
        - ay -> ay (not initial y)
        - oay -> oay (not initial y)
        """
        try:
            diacritic = Vietnamese.y_s.index(rhyme[0])
        except ValueError:
            return rhyme
        else:
            return Vietnamese.i_s[diacritic] + rhyme[1:]
    
    def i2y(rhyme: str):
        """
        Change the initial `i` to `y`, example:
        - iên -> yên
        - ĩ -> ỹ
        - iếm -> yếm
        - ai -> ai (not initial i)
        - oai -> oai (not initial i)
        """
        try:
            diacritic = Vietnamese.i_s.index(rhyme[0])
        except ValueError:
            return rhyme
        else:
            return Vietnamese.y_s[diacritic] + rhyme[1:]
        
    @staticmethod
    def clean_trash(word: str):
        trashes = ['.', ',', '-', ' ']
        for trash in trashes:
            word = word.replace(trash, '')
        return word
    
    @staticmethod
    def diacritic(word: str):
        """Return the diacritic number of a word, the index in the word which the diacritic occurs, and the vowel index on `Vietnamese.diacritic_{n}_chars`.
        
        Note that diacritic is different from tone, 
        and `diacritic` here is the tone-related diacritics (the acute, grave, hook, tilde, or underdot)
        , not the diacritics like in `â`, `ă`, `ư`, ...
        
        The `diacritic` values are:
        - 0: No diacritic (in this case, it will return `(0, None, None)`)
        - 1: Acute detected: Can be tone 1 or tone 6
        - 2: Grave detected: Tone 2
        - 3: Hook detected: Tone 3
        - 4: Tilde detected: Tone 4
        - 5: Underdot detected: Can be tone 5 or tone 7
        
        If multiple diacritics are present, the function will return `(None, None, None)` because this is not a Vietnamese word.
        
        """
        
        current_diacritic = 0
        idx_in_word = 0
        char_idx = 0
        occurences = 0
        for idx, char in enumerate(word):
            if occurences > 1:
                # Not a Vietnamese word
                return None, None, None
            if char in Vietnamese.diacritic_1_chars:
                char_idx = Vietnamese.diacritic_1_chars.index(char)
                occurences += 1
                current_diacritic = 1
                idx_in_word = idx
            elif char in Vietnamese.diacritic_2_chars:
                char_idx = Vietnamese.diacritic_2_chars.index(char)
                occurences += 1
                current_diacritic = 2
                idx_in_word = idx
            elif char in Vietnamese.diacritic_3_chars:
                char_idx = Vietnamese.diacritic_3_chars.index(char)
                occurences += 1
                current_diacritic = 3
                idx_in_word = idx
            elif char in Vietnamese.diacritic_4_chars:
                char_idx = Vietnamese.diacritic_4_chars.index(char)
                occurences += 1
                current_diacritic = 4
                idx_in_word = idx
            elif char in Vietnamese.diacritic_5_chars:
                char_idx = Vietnamese.diacritic_5_chars.index(char)
                occurences += 1
                current_diacritic = 5
                idx_in_word = idx
        
        if current_diacritic == 0:
            idx_in_word, char_idx = None, None
            
        return current_diacritic, idx_in_word, char_idx
            
    @staticmethod
    def analyze(word: str) -> tuple[str, str, int] | tuple[str, None, None]:
        """
        Return the consonant family, rhyme family, and tone of the word. If the word is not recognized as a Vietnamese word, return `(word, None, None)` instead.
        - Consonant families: ∈`Vietnamese.consonant_families` 
            - `q`, `c`, `k` -> `k`
            - `ng`, `ngh` -> `ng`
            - `g`, `gh` -> `g`
            - `gi` -> `z`
            - `None` -> `0`
        - Rhyme families (`a`, `á`, `à`, `ả`, `ã`, `ạ` are all in `a` family): ∈`Vietnamese.rhymes_families` 
            - `i`, `y` -> `i`
            - `iên`, `yên` -> `iên`
            - `iêng`, `yêng` -> `iêng`
            - `iêm`, `yêm` -> `iêm`
            - `*t`, `*n` -> `*n`
            - `*c`, `*ng` -> `*ng`
            - `*p`, `*m` -> `*m`
            - `*ch`, `*nh` -> `*nh`
        - Tones: ∈`[0, 1, 2, 3, 4, 5, 6, 7]`
        
        """
        original_word = word
        diacritic, idx_in_word, char_idx = Vietnamese.diacritic(word)
        if diacritic is None:
            return original_word, None, None
        
        # Replace character with diacritic with its non-diacritic counterpart
        if idx_in_word is not None:
            word = word[:idx_in_word] + Vietnamese.diacritic_0_chars[char_idx] + word[idx_in_word+1:]
        original_word_no_diacritic = word
        
        # Replace final consonants that indicate tone 6 and 7
        if diacritic == 1 or diacritic == 5:
            word = word[:-1] + word[-1].replace('t', 'n').replace('c', 'ng').replace('p', 'm')
            if word[-2:] == 'ch':
                word = word[:-2] + 'nh'
            if original_word_no_diacritic != word and diacritic == 1:
                diacritic = 6
            elif original_word_no_diacritic != word and diacritic == 5:
                diacritic = 7
        
        tone = diacritic
        
        # Now 'word' is clean (in the structure of CONSONANT+RHYME_FAMILY)
        if word in Vietnamese.rhymes_families_isolated:
            return '0', Vietnamese.y2i(word), tone
        if word[:1] == 'c' and word[1:] in Vietnamese.rhymes_families_with_c:
            return 'k', word[1:], tone
        if word[:1] == 'q' and word[1:] in Vietnamese.rhymes_families_with_q:
            # `qua` is actually `koa`, `quen` is actually `koen`, quau is actually `koau`, `queo` is actually `koeo`
            if word[2] == 'a' or word[2] == 'ă' or word[2] == 'e':
                return 'k', 'o' + word[2:], tone
            if word[1:] == 'ui':
                return 'k', 'uy', tone
            if word[1:] == 'uin':
                return 'k', 'uyn', tone
            return 'k', word[1:], tone
        if word[:1] == 'k' and word[1:] in Vietnamese.rhymes_families_with_k:
            return 'k', Vietnamese.y2i(word[1:]), tone
        if word[:1] == 'g' and word[1:] in Vietnamese.rhymes_families_with_g:
            return 'g', word[1:], tone
        if word[:2] == 'ng' and word[2:] in Vietnamese.rhymes_families_with_ng:
            return 'ng', word[2:], tone
        if word[:2] == 'gh' and word[2:] in Vietnamese.rhymes_families_with_ngh_gh:
            return 'g', word[2:], tone
        if word[:3] == 'ngh' and word[3:] in Vietnamese.rhymes_families_with_ngh_gh:
            return 'ng', word[3:], tone
        if word[:2] == 'gi' and word[2:] in Vietnamese.rhymes_families_with_gi:
            # `gi` is z+i
            if word[2:] == '':
                return 'z', 'i', tone
            # `gin` is z+in
            elif word[2:] == 'n':
                return 'z', 'in', tone
            # `giết`, `giêng`
            elif word[2:] == 'ên' or word[2:] == 'êng':
                return 'z', 'i' + word[2:], tone
            return 'z', word[2:], tone
        if word[:1] in Vietnamese.other_consonants and word[1:] in Vietnamese.rhymes_families_with_other_consonants:
            return word[:1], Vietnamese.y2i(word[1:]), tone
        if word[:2] in Vietnamese.other_consonants and word[2:] in Vietnamese.rhymes_families_with_other_consonants:
            return word[:2], Vietnamese.y2i(word[2:]), tone
        
        # No match with Vietnamese structure
        return original_word, None, None
