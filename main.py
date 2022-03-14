import helper_functions as hpf
import lp_text as lp
import testing_texts as tt
import book_texts as bt
import encryption as enc

if __name__ == '__main__':
    # ct =lp.get_unsolved_pages()
    ct = enc.random_otp(bt.return_alice_plaintext())
    hpf.print_section_info(ct)
    hpf.calculate_ioc(ct)
    hpf.count_doublets(ct)
    hpf.plot_bigrams(ct, 'runes')
    hpf.plot_letter_frequency(ct, 'latin')
