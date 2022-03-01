import helper_functions as hpf
import lp_text as lp
import testing_texts as tt

if __name__ == '__main__':
    ct = tt.test_autokey_mortlach_1()
    hpf.print_section_info(ct)
    hpf.calculate_ioc(ct)
    hpf.count_doublets(ct)
    hpf.plot_bigrams(ct, 'runes','fullscreen')
    hpf.plot_letter_frequency(ct, 'latin')
