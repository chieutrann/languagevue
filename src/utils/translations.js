// Translation content for different languages
const translations = {
  en: {
    // Navigation
    nav_news: "News",
    nav_vocabulary: "Vocabulary",
    nav_dictionary: "Dictionary",
    nav_folders: "VocabVault",
    
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
    folders_title: "Vocabulary Folders",
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
    
    // Messages
    msg_loading: "Loading...",
    msg_error: "An error occurred",
    msg_success: "Operation successful",
    msg_no_results: "No results found",
    msg_confirm_delete: "Are you sure you want to delete this item?",
    
    // Alert Messages
    alert_word_exists: "This word already exists in this folder!",
    alert_folder_exists: "A folder with this name already exists!",
    alert_no_word: "Please enter a word",
    alert_no_definition: "Please enter a definition",
    alert_save_success: "Successfully saved!",
    alert_delete_success: "Successfully deleted!",
    alert_error: "An error occurred. Please try again.",
    alert_confirm_delete: "Are you sure you want to delete this item?",
    alert_translation_fail: "Translation failed. Please try again.",
    alert_required_field: "This field is required",
    alert_network_error: "Network error. Please check your connection.",
    alert_server_error: "Server error. Please try again later."
  },
  vi: {
    // Navigation
    nav_news: "Tin tức",
    nav_vocabulary: "Từ vựng",
    nav_dictionary: "Từ điển",
    nav_folders: "Kho từ vựng",
    
    // Headers
    header_title: "Tin tức học tiếng Đức",
    header_subtitle: "Học tiếng Đức qua tin tức hiện tại",
    
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
    folders_title: "Kho từ vựng",
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
    
    // Messages
    msg_loading: "Đang tải...",
    msg_error: "Đã xảy ra lỗi",
    msg_success: "Thao tác thành công",
    msg_no_results: "Không tìm thấy kết quả",
    msg_confirm_delete: "Bạn có chắc chắn muốn xóa mục này không?",
    
    // Alert Messages
    alert_word_exists: "Từ này đã tồn tại trong thư mục!",
    alert_folder_exists: "Thư mục với tên này đã tồn tại!",
    alert_no_word: "Vui lòng nhập từ",
    alert_no_definition: "Vui lòng nhập định nghĩa",
    alert_save_success: "Lưu thành công!",
    alert_delete_success: "Xóa thành công!",
    alert_error: "Đã xảy ra lỗi. Vui lòng thử lại.",
    alert_confirm_delete: "Bạn có chắc chắn muốn xóa mục này?",
    alert_translation_fail: "Dịch thất bại. Vui lòng thử lại.",
    alert_required_field: "Trường này là bắt buộc",
    alert_network_error: "Lỗi mạng. Vui lòng kiểm tra kết nối.",
    alert_server_error: "Lỗi máy chủ. Vui lòng thử lại sau."
  }
}

export function getTranslation(key, lang = 'en') {
  return translations[lang]?.[key] || translations.en[key] || key
}

export function useTranslations(lang = 'en') {
  return {
    t: (key) => getTranslation(key, lang),
    translations: translations[lang] || translations.en
  }
}

export { translations }
