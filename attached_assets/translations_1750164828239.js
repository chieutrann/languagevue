// Translation content for different languages
const translations = {
    en: {
        // Navigation
        nav_news: "News",
        nav_vocabulary: "Vocabulary",
        nav_dictionary: "Dictionary",
        nav_definition: '📖 Definition',
        nav_conjugation: '⚡ Conjugation',
        nav_lookup: '🔍 Lookup',
        nav_examples: '💡 Examples',
        nav_browse: '📚 Browse',
        nav_folders: '📂 VocabVault',
        
        // Headers
        header_title: "German Learning News",
        header_subtitle: "Learn German through current events",
    

        
        // Dictionary page
        dict_search_placeholder: "Search for a German word...",
        dict_word_type: "Word Type",
        dict_translation: "Translation",
        dict_examples: "Examples",
        dict_conjugation: "Conjugation",
        dict_no_results: "No results found",
        dict_loading: "Loading...",
        
        // Vocabulary page
        vocab_title: "Vocabulary List",
        vocab_add_new: "Add New Word",
        vocab_german: "German",
        vocab_translation: "Translation",
        vocab_type: "Type",
        vocab_actions: "Actions",

        
        // Folders 
        title_folders: "Vocabulary Vault",
        folders_title: "Vocabulary Folders",
        folder_add_new: "Add New Folder",
        folder_name: "Folder Name",
        folder_description: "Description",
        folder_actions: "Actions",
        folder_no_results: "No results found",
        folder_name_already_exists:"Folder name already exists",
        folder_name_required:"Folder name is required",

        //Folder
        folder_title: "Folder",
        folder_add_new: "Add New Folder",
        folder_name: "Folder Name",
        folder_description: "Description",
        folder_actions: "Actions",
        folder_no_results: "No results found",
    
        
        // Word types
        type_noun: "Noun",
        type_verb: "Verb",
        type_adjective: "Adjective",
        type_adverb: "Adverb",
        type_preposition: "Preposition",
        
        // Difficulty levels
        diff_beginner: "Beginner",
        diff_intermediate: "Intermediate",
        diff_advanced: "Advanced",
        
        // Buttons
        btn_search: "Search",
        btn_clear: "Clear",
        btn_add: "Add",
        btn_edit: "Edit",
        btn_delete: "Delete",
        btn_save: "Save",
        btn_cancel: "Cancel",
        btn_conjugate: 'Conjugate',
        btn_lookup: 'Lookup',
        btn_examples: 'Get Examples',
        btn_random: '🎲 Random Words',
        btn_stats: '📊 Statistics',
        
        // Messages
        msg_loading: "Loading...",
        msg_error: "An error occurred",
        msg_success: "Operation successful",
        msg_no_results: "No results found",
        msg_confirm_delete: "Are you sure you want to delete this item?",
        
        // Titles
        title_definition: '📖 Word Definition',
        title_conjugation: '⚡ Verb Conjugation',
        title_lookup: '🔍Dictionary Lookup',
        additional_features:"Additional Features",
        title_examples: '💡 Word Examples',
        title_browse: '📚 Browse Dictionary',
        title_random: 'Random Words',
        title_stats: 'Dictionary Statistics',
        
        // Descriptions
        desc_definition: 'Search for German words and get detailed definitions with translations',
        desc_conjugation: 'Get complete conjugation forms for any German verb',
        desc_lookup: 'Get comprehensive word data (Digital Dictionary of German)',
        desc_examples: 'Get practical examples and usage patterns',
        desc_browse: 'Explore words by type, difficulty, or get random selections',
        
        // Placeholders
        placeholder_definition: 'Enter a German word for definition...',
        placeholder_conjugation: 'Enter a German verb to conjugate...',
        placeholder_lookup: 'Enter a German word...',
        placeholder_examples: 'Enter a German word for examples...',
        
        // Categories
        category_types: 'Word Types',
        category_difficulty: 'Difficulty Levels',
        
        // Results
        result_definition: 'Definition Result',
        result_conjugation: 'Conjugation Result',
        result_lookup: 'Lookup Result',
        result_examples: 'Example Sentences',
        
        // Loading States
        loading_definition: 'Looking up word definition...',
        loading_conjugation: 'Generating conjugation forms...',
        loading_lookup: 'Fetching data...',
        loading_examples: 'Finding example sentences...',
        loading_random: 'Getting random words...',
        loading_type: 'Loading words by type...',
        loading_difficulty: 'Loading words by difficulty...',
        loading_stats: 'Loading dictionary statistics...',
        
        // Other
        german_definition: 'German Definition',
        total_words: 'Total Words',

        // Alert Messages
        alert_word_exists: "This word already exists in this folder!",
        alert_folder_exists: "A folder with this name already exists!",
        alert_no_word: "Please enter a word",
        alert_no_definition: "Please enter a definition",
        alert_save_success: "Successfully saved!",
        alert_delete_success: "Successfully deleted!",
        alert_error: "An error occurred. Please try again.",
        alert_confirm_delete: "Are you sure you want to delete this item?",
        alert_audio_fail: "Failed to load audio. Please try again.",
        alert_no_audio: "No audio available for this word.",
        alert_translation_fail: "Translation failed. Please try again.",
        alert_required_field: "This field is required",
        alert_invalid_input: "Invalid input. Please check and try again.",
        alert_network_error: "Network error. Please check your connection.",
        alert_server_error: "Server error. Please try again later.",
        alert_login_required: "Please log in to access this feature."
    },
    vi: {
        // Navigation
        nav_news: "Tin tức",
        nav_vocabulary: "Từ vựng",
        nav_dictionary: "Từ điển",
        nav_definition: '📖 Định nghĩa',
        nav_conjugation: '⚡ Chia động từ',
        nav_lookup: '🔍 Tra Từ',
        nav_examples: '💡 Ví dụ',
        nav_browse: '📚 Duyệt',
        nav_folders: '📂 Kho từ vựng',

        // Headers
        header_title: "Tin tức học tiếng Đức",
        header_subtitle: "Học tiếng Đức qua tin tức hiện tại",
        header_folders: "Kho từ vựng",
        
        // Dictionary page
        dict_search_placeholder: "Tìm kiếm từ tiếng Đức...",
        dict_word_type: "Loại từ",
        dict_translation: "Bản dịch",
        dict_examples: "Ví dụ",
        dict_conjugation: "Chia động từ",
        dict_no_results: "Không tìm thấy kết quả",
        dict_loading: "Đang tải...",
        
        // Vocabulary page
        vocab_title: "Danh sách từ vựng",
        vocab_add_new: "Thêm từ mới",
        vocab_german: "Tiếng Đức",
        vocab_translation: "Bản dịch",
        vocab_type: "Loại",
        vocab_actions: "Thao tác",
        
        // Folders 
        title_folders: "Kho từ vựng",
        folders_title: "Kho từ vựng",
        folder_add_new: "Thêm kho từ vựng",
        folder_name: "Tên kho từ vựng",
        folder_description: "Mô tả kho từ vựng",
        folder_actions: "Thao tác",
        folder_no_results: "Không tìm thấy kết quả",
        folder_name_already_exists: "Tên kho từ vựng đã tồn tại",

        //Folder
        folder_title: "Kho từ vựng",
        folder_add_new: "Thêm kho từ vựng",
        folder_name: "Tên kho từ vựng",
        folder_description: "Mô tả kho từ vựng",
        folder_actions: "Thao tác",
        folder_no_results: "Không tìm thấy kết quả",
        
        // Word types
        type_noun: "Danh từ",
        type_verb: "Động từ",
        type_adjective: "Tính từ",
        type_adverb: "Trạng từ",
        type_preposition: "Giới từ",
        
        // Difficulty levels
        diff_beginner: "Cơ bản",
        diff_intermediate: "Trung cấp",
        diff_advanced: "Nâng cao",
        
        // Buttons
        btn_search: "Tìm kiếm",
        btn_clear: "Xóa",
        btn_add: "Thêm",
        btn_edit: "Sửa",
        btn_delete: "Xóa",
        btn_save: "Lưu",
        btn_cancel: "Hủy",
        btn_conjugate: 'Chia động từ',
        btn_lookup: 'Tra Từ Điển',
        btn_examples: 'Xem ví dụ',
        btn_random: '🎲 Từ ngẫu nhiên',
        btn_stats: '📊 Thống kê',
        
        // Messages
        msg_loading: "Đang tải...",
        msg_error: "Đã xảy ra lỗi",
        msg_success: "Thao tác thành công",
        msg_no_results: "Không tìm thấy kết quả",
        msg_confirm_delete: "Bạn có chắc chắn muốn xóa mục này không?",
        
        // Titles
        title_definition: '📖 Định nghĩa từ',
        title_conjugation: '⚡ Chia động từ',
        title_lookup: '🔍 Tra từ điển',
        additional_features:"Tính năng bổ sung",
        title_examples: '💡 Ví dụ từ vựng',
        title_browse: '📚 Duyệt từ điển',
        title_random: 'Từ ngẫu nhiên',
        title_stats: 'Thống kê từ điển',
        
        // Descriptions
        desc_definition: 'Tìm kiếm từ tiếng Đức và xem định nghĩa chi tiết với bản dịch',
        desc_conjugation: 'Xem các dạng chia của động từ tiếng Đức',
        desc_lookup: 'Xem dữ liệu từ chi tiết từ từ điển',
        desc_examples: 'Xem các ví dụ và cách sử dụng',
        desc_browse: 'Khám phá từ vựng theo loại, độ khó hoặc chọn ngẫu nhiên',
        
        // Placeholders
        placeholder_definition: 'Nhập từ tiếng Đức để tra nghĩa...',
        placeholder_conjugation: 'Nhập động từ tiếng Đức để chia...',
        placeholder_lookup: 'Nhập từ tiếng Đức để tra...',
        placeholder_examples: 'Nhập từ tiếng Đức để xem ví dụ...',
        
        // Categories
        category_types: 'Loại từ',
        category_difficulty: 'Độ khó',
        
        // Results
        result_definition: 'Kết quả định nghĩa',
        result_conjugation: 'Kết quả chia động từ',
        result_lookup: 'Kết quả tra',
        result_examples: 'Câu ví dụ',
        
        // Loading States
        loading_definition: 'Đang tra nghĩa...',
        loading_conjugation: 'Đang chia động từ...',
        loading_lookup: 'Đang tải dữ liệu...',
        loading_examples: 'Đang tìm câu ví dụ...',
        loading_random: 'Đang tải từ ngẫu nhiên...',
        loading_type: 'Đang tải từ theo loại...',
        loading_difficulty: 'Đang tải từ theo độ khó...',
        loading_stats: 'Đang tải thống kê...',
        
        // Other
        german_definition: 'Định nghĩa tiếng Đức',
        total_words: 'Tổng số từ',

        // Alert Messages
        alert_word_exists: "Từ này đã tồn tại trong thư mục!",
        alert_folder_exists: "Thư mục với tên này đã tồn tại!",
        alert_no_word: "Vui lòng nhập từ",
        alert_no_definition: "Vui lòng nhập định nghĩa",
        alert_save_success: "Lưu thành công!",
        alert_delete_success: "Xóa thành công!",
        alert_error: "Đã xảy ra lỗi. Vui lòng thử lại.",
        alert_confirm_delete: "Bạn có chắc chắn muốn xóa mục này?",
        alert_audio_fail: "Không thể tải âm thanh. Vui lòng thử lại.",
        alert_no_audio: "Không có âm thanh cho từ này.",
        alert_translation_fail: "Dịch thất bại. Vui lòng thử lại.",
        alert_required_field: "Trường này là bắt buộc",
        alert_invalid_input: "Dữ liệu không hợp lệ. Vui lòng kiểm tra và thử lại.",
        alert_network_error: "Lỗi mạng. Vui lòng kiểm tra kết nối.",
        alert_server_error: "Lỗi máy chủ. Vui lòng thử lại sau.",
        alert_login_required: "Vui lòng đăng nhập để truy cập tính năng này."
    }
};

// Function to get translation for a key
function getTranslation(key) {
    const currentLang = localStorage.getItem('preferredLanguage') || 'en';
    return translations[currentLang][key] || key;
}

// Function to update all translatable elements on the page
function updatePageTranslations() {
    // Update navigation
    document.querySelector('nav a[href="/"]').textContent = "📰 " + getTranslation('nav_news');
    document.querySelector('nav a[href="/vocabulary"]').textContent = "📚 " + getTranslation('nav_vocabulary');
    document.querySelector('nav a[href="/dictionary"]').textContent = "📖 " + getTranslation('nav_dictionary');
    
    // Update headers
    document.querySelector('h1').textContent = "🇩🇪 " + getTranslation('header_title');
    document.querySelector('.subtitle').textContent = getTranslation('header_subtitle');
    
    // Update all elements with data-translate attribute
    document.querySelectorAll('[data-translate]').forEach(element => {
        const key = element.getAttribute('data-translate');
        if (element.tagName === 'INPUT' || element.tagName === 'TEXTAREA') {
            if (element.getAttribute('placeholder')) {
                element.setAttribute('placeholder', getTranslation(key));
            }
        } else {
            element.textContent = getTranslation(key);
        }
    });
}

// Function to translate word types
function translateWordType(type) {
    const typeKey = 'type_' + type.toLowerCase();
    return getTranslation(typeKey);
}

// Function to translate difficulty levels
function translateDifficulty(difficulty) {
    const diffKey = 'diff_' + difficulty.toLowerCase();
    return getTranslation(diffKey);
}

// Function to update dynamic content translations
function updateDynamicTranslations() {
    // Update word types in dropdowns or lists
    document.querySelectorAll('[data-word-type]').forEach(element => {
        const type = element.getAttribute('data-word-type');
        element.textContent = translateWordType(type);
    });
    
    // Update difficulty levels
    document.querySelectorAll('[data-difficulty]').forEach(element => {
        const difficulty = element.getAttribute('data-difficulty');
        element.textContent = translateDifficulty(difficulty);
    });
}

// Initialize translations when DOM is loaded
document.addEventListener('DOMContentLoaded', () => {
    updatePageTranslations();
    updateDynamicTranslations();
});

// Listen for language changes
document.getElementById('targetLang')?.addEventListener('change', () => {
    updatePageTranslations();
    updateDynamicTranslations();
    updateVisibleTranslations(); // This is the function from base.html that updates translations
}); 