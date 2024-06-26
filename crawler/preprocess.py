'''
    This file is for preprocessing data from crawler.
    With data store in folder ./data/thutuchanhchinh, we will create a new folder data/thutuchanhchinh_preprocessed.
'''
import os
import json
import bs4
import time

'''
    Helper Functions
'''

folder_name = "thutuchanhchinh_preprocessed2"

def create_drop_data():
    for file in os.listdir(f"./data/{folder_name}"):
        os.remove(os.path.join(f"./data/{folder_name}", file))

    os.removedirs(f"./data/{folder_name}")
    time.sleep(3)
    os.makedirs(f"./data/{folder_name}")


def prompt_basic_info(id, ten, soqd, capthuchien, loaithutuc, linhvuc):
    prompt = "Thủ tục hành chính tên " + ten + " có các thông tin về  tên, số quyết định, cấp thực hiện, loại thủ tục và lĩnh vực như sau ::\n"
    prompt += f"Thủ tục hành chính này được ban hành theo quyết định số {soqd}, thủ tục hành chính này được thực hiện ở các cấp: {capthuchien}"
    prompt += f". Nó thuộc loại thủ tục là {loaithutuc} và thuộc lĩnh vực {linhvuc}.\n"
    prompt += "\n"
    return prompt


def prompt_trinhtu_thuchien(id, ten, trinhtuthuchien):
    prompt = f"Cần làm theo trình tự các bước sau để thực hiện thủ tục hành chính {ten} ::\n"
    prompt += trinhtuthuchien.replace("       ", "\n")
    prompt += "\n\n"
    return prompt

def prompt_cachthuc_thuchien(ten, cachthucthuchiens):
    if not cachthucthuchiens or len(cachthucthuchiens) == 0:
        return f"Thủ tục hành chính {ten} chưa có mô tả cách thức thực hiện nào.\n\n"
    prompt = f"Có những cách thức thực hiện sau để làm thủ tục hành chính {ten} ::\n"
    for cachthuc in cachthucthuchiens:
        prompt += f"- Với hình thức {cachthuc['hinhthucnop']}, thời gian giải quyết sẽ là {cachthuc['thoigiangiaiquyet']}. Cách thức thực hiện này sẽ có mô tả như sau: {cachthuc['mota']}\n"
    prompt += "\n"
    return prompt

def prompt_thanhphan_hoso(ten, thanhphanhosos, diachitiepnhanhs):
    prompt = f"Cần các hồ sơ sau đây làm thủ tục hành chính {ten} và nộp tại địa điểm nơi sau ::\n"
    for index, hoso in enumerate(thanhphanhosos):
        if 'ghichu' in hoso.keys():
            prompt += f"- Ghi chú: {hoso['ghichu']}\n"
            continue
        prompt += f"{index + 1}. {hoso['ten']}: cần {hoso['banchinh']} bản chính và {hoso['bansao']} bản sao."
        maudon_element = bs4.BeautifulSoup(hoso["maudon"], "html.parser").find("a")

        if not maudon_element.has_attr("href") and maudon_element["href"] != '':
            prompt += ". Với hồ sơ này hiện tại chưa có mẫu đơn nào.\n"
        else:
            link = maudon_element["href"].strip()
            prompt += f". Mẫu đơn cho hồ sơ này có thể tìm thấy tại {link}\n"
    prompt += "\n"
    return prompt

def prompt_coquan_tochuc(ten, doituongthuchien, coquanthuchien, coquanphoihop, coquanthamquyen, coquanuyquyen, diachitiepnhanhs, ketquathuchien, yeucaudieukien):
    prompt = f"Cơ quan thực hiện, ủy quyền, thẩm quyền, điều kiện thực hiện, kết quả thực hiện của thủ tục hành chính {ten} như sau::\n"
    prompt += f"- Cơ quan thực hiện: {coquanthuchien}\n"
    prompt += f"- Cơ quan thẩm quyền: {coquanthamquyen}\n"
    prompt += f"- Cơ quan ủy quyền: {coquanuyquyen}\n"
    prompt += f"- Cơ quan phối hợp: {coquanphoihop}\n"
    prompt += f"Để thực hiện thủ tục hành chính {ten}, đối tượng được phép thực hiện là {doituongthuchien} và cần đảm bảo điều kiện sau đây:  {yeucaudieukien}. Hồ sơ cần được nộp tại {diachitiepnhanhs}. Sau khi thực hiện thủ tục, kết quả sẽ là {ketquathuchien}\n"
    prompt += "\n"
    return prompt

def prompt_cancu_phaply(ten, cancuphaplys):
    prompt = f"Trích dẫn pháp luật, căn cứ pháp lý dựa vào các văn bản pháp luật của thủ tục hành chính {ten} như sau::\n"
    for index, cancuphaply in enumerate(cancuphaplys):
        prompt += f"{index + 1}. Số ký hiệu {cancuphaply['sokyhieu']}, có trích yếu là {cancuphaply['trichyeu']}, được ban hành từ ngày {cancuphaply['ngaybanhanh']}. Cơ quan ban hành là {cancuphaply['coquanbanhanh'] or 'chưa rõ'}\n"
    prompt += "\n"
    return prompt

'''
    Main Function
'''

def main():
    create_drop_data()
    for file in os.listdir("./data/thutuchanhchinh"):
        # try:
            if not file.endswith(".json"):
                continue
            with open(os.path.join("./data/thutuchanhchinh", file), "r") as f:
                data = json.load(f)
                f.close()
            text = ""
            # Remove all spaces and new line characters at the end of string.
            id = data["id"].strip()
            ten = data["ten"].strip()
            soqd = data["soqd"].strip()
            capthuchien = data["capthuchien"].strip()
            loaithutuc = data["loaithutuc"].strip()
            linhvuc = data["linhvuc"].strip()
            data["trinhtuthuchien"] = data["trinhtuthuchien"].strip()
            data["trinhtuthuchien"] = data["trinhtuthuchien"].replace("\n\n", "")
            trinhtuthuchien = data["trinhtuthuchien"]
            for cachthuc in data["cachthucthuchiens"]:
                cachthuc["hinhthucnop"] = cachthuc["hinhthucnop"].strip()
                cachthuc["thoigiangiaiquyet"] = cachthuc["thoigiangiaiquyet"].strip()
                cachthuc["thoigiangiaiquyet"] = cachthuc["thoigiangiaiquyet"].replace("\n\n", "")
                cachthuc["mota"] = cachthuc["mota"].strip()
                cachthuc["mota"] = cachthuc["mota"].replace("\n\n", "")
                cachthuc["phi"] = cachthuc["phi"].strip()
            for hoso in data["thanhphanhosos"]:
                if 'ghichu' in hoso.keys() :
                    hoso["ghichu"] = hoso["ghichu"].strip()
                    continue
                hoso["ten"] = hoso["ten"].strip()
                hoso["banchinh"] = hoso["banchinh"].strip()
                hoso["bansao"] = hoso["bansao"].strip()
                hoso["maudon"] = hoso["maudon"].strip()
            doituongthuchien = data["doituongthuchien"].strip()
            coquanthuchien = data["coquanthuchien"].strip()
            coquanthamquyen = data["coquanthamquyen"].strip()
            coquanuyquyen = data["coquanuyquyen"].strip()
            coquanphoihop = data["coquanphoihop"].strip()
            diachitiepnhanhs = data["diachitiepnhanhs"].strip()
            ketquathuchien = data["ketquathuchien"].strip()
            yeucaudieukien = data["yeucaudieukien"].strip()

            text += prompt_basic_info(id, ten, soqd, capthuchien, loaithutuc, linhvuc)
            text += prompt_trinhtu_thuchien(id, ten, trinhtuthuchien)
            text += prompt_cachthuc_thuchien(ten, data["cachthucthuchiens"])
            text += prompt_thanhphan_hoso(ten, data["thanhphanhosos"], diachitiepnhanhs)
            text += prompt_coquan_tochuc(
                ten, doituongthuchien, coquanthuchien, coquanphoihop, coquanthamquyen, coquanuyquyen, diachitiepnhanhs, ketquathuchien, yeucaudieukien
            )
            text += prompt_cancu_phaply(ten, data["cancuphaplys"])

            with open(f"./data/{folder_name}/" + file.replace(".json", ".txt"), "w") as f:
                f.write(text)
                f.close()
        # except Exception as e:
        #     print(e)
        #     print("Error at file: " + file)
        #     continue


if __name__ == "__main__":
    main()

