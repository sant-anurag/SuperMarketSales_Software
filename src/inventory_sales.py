import os

from app_defines import *
from app_common import *
from app_thread import *
from customer_details import *
import smtplib
from email.message import EmailMessage


class InventorySales:

    # constructor for Library class
    def __init__(self, master):
        self.obj_commonUtil = CommonUtil()
        self.dateTimeOp = DatetimeOperation()
        self.sales_window = Toplevel(master)
        self.sales_window.title("Sales")
        self.sales_window.geometry('1300x750+240+150')
        self.sales_window.configure(background='wheat')
        self.sales_window.resizable(width=False, height=False)
        self.sales_window.protocol('WM_DELETE_WINDOW', self.obj_commonUtil.donothing)
        self.list_InvoicePrint = []
        self.list_productDetails = []
        canvas_width, canvas_height = 1300, 750
        canvas = Canvas(self.sales_window, width=canvas_width, height=canvas_height)
        myimage = ImageTk.PhotoImage(
            PIL.Image.open("..\\Images\\Logos\\Geometry-Header-1920x1080.jpg"))
        canvas.create_image(0, 0, anchor=NW, image=myimage)
        canvas.pack()

        self.dataModifyFrame = Frame(self.sales_window, width=800, height=500, bd=2, relief='ridge',
                                     bg='snow')
        self.dataModifyFrame.pack()
        self.dataSearchFrame = Frame(self.sales_window, width=800, height=500, bd=2, relief='ridge',
                                     bg='snow')
        self.dataSearchFrame.pack()
        self.frameupper = Frame(self.sales_window, width=1140, height=100, bd=2, relief='ridge',
                                bg='snow')
        self.frameupper.pack()
        self.billAreaFrame = Frame(self.dataSearchFrame, relief=GROOVE, width=520, height=407, bd=2)
        self.billAreaFrame.pack()

        self.searchproductDeatilsArea = Frame(self.sales_window, relief=GROOVE, width=1290, height=150, bd=2)
        self.searchproductDeatilsArea.pack()

        # Main button frame design for Add to cart, Bill, Reset, and Exit Screen-start
        self.MainbtnFrame = Frame(self.sales_window, width=148, height=215, bd=4, relief='ridge',
                                  bg='wheat')
        self.btn_addToCart = Button(self.MainbtnFrame)
        self.btn_addToCart.configure(text="Add To Cart", fg="Black", font=NORM_FONT, width=14, state=NORMAL,
                                     bg='RosyBrown1')
        self.btn_submit = Button(self.MainbtnFrame)
        self.btn_submit.configure(text="Tender Bill", fg="Black", font=NORM_FONT, width=14, state=NORMAL,
                                  bg='RosyBrown1')
        self.btn_reset = Button(self.MainbtnFrame, text="Reset Item", fg="Black",
                                font=NORM_FONT, width=14, state=DISABLED, bg='light grey')
        resetcart_result = partial(self.resetcart)
        self.btn_resetCart = Button(self.MainbtnFrame, text="Reset Cart", fg="Black",
                                    font=NORM_FONT, width=14, command=resetcart_result, state=DISABLED, bg='light grey')
        self.btn_print = Button(self.MainbtnFrame, text="Print Invoice", fg="Black",
                                font=NORM_FONT, width=14, state=DISABLED, bg='light grey')

        mainmenu_label = Label(self.MainbtnFrame, text="Main Menu", width=12, justify=CENTER,
                               font=L_FONT,
                               bg='wheat')

        self.MainbtnFrame.place(x=5, y=5)
        mainmenu_label.place(x=2, y=5)
        self.btn_addToCart.place(x=2, y=40)
        self.btn_submit.place(x=2, y=73)
        self.btn_reset.place(x=2, y=106)
        self.btn_resetCart.place(x=2, y=139)
        self.btn_print.place(x=2, y=172)

        # Support button frame design -start
        self.AdditionalbtnFrame = Frame(self.sales_window, width=148, height=285, bd=4, relief='ridge',
                                        bg='wheat')
        opmenu_label = Label(self.AdditionalbtnFrame, text="Context Menu", width=12, justify=CENTER,
                             font=L_FONT,
                             bg='wheat')
        self.btn_chgQuantity = Button(self.AdditionalbtnFrame)
        chngQuantity_result = partial(self.change_quantity_display)
        self.btn_chgQuantity.configure(text="Change Quantity", fg="Black", font=NORM_FONT, width=14, state=DISABLED,
                                       bg='light grey', command=chngQuantity_result)
        self.btn_discount = Button(self.AdditionalbtnFrame)
        discount_result = partial(self.discount_display)
        self.btn_discount.configure(text="Discount %", fg="Black", font=NORM_FONT, width=14, state=DISABLED,
                                    bg='light grey', command=discount_result)
        self.btn_tax = Button(self.AdditionalbtnFrame)
        tax_result = partial(self.tax_display)
        self.btn_tax.configure(text="Tax %", fg="Black", font=NORM_FONT, width=14, state=DISABLED,
                               bg='light grey', command=tax_result)
        remove_result = partial(self.removeItem_display)
        self.btn_remItem = Button(self.AdditionalbtnFrame, text="Remove Item", fg="Black",
                                  font=NORM_FONT, width=14, state=DISABLED, bg='light grey', command=remove_result)
        redeem_result = partial(self.redeemPoints_display)
        self.btn_redeempts = Button(self.AdditionalbtnFrame, text="Redeem Points", fg="Black",
                                    font=NORM_FONT, width=14, state=DISABLED, bg='light grey', command=redeem_result)
        shopper_result = partial(self.customer_operations)
        self.btn_member = Button(self.AdditionalbtnFrame, text="Shopper", fg="Black",
                                 font=NORM_FONT, width=14, state=NORMAL, bg='RosyBrown1', command=shopper_result)
        self.btn_exit = Button(self.AdditionalbtnFrame, text="Exit", fg="Black",
                               font=NORM_FONT, width=14, state=NORMAL, bg='RosyBrown1')
        self.btn_exit.configure(command=self.sales_window.destroy)

        self.AdditionalbtnFrame.place(x=5, y=220)
        opmenu_label.place(x=2, y=5)
        self.btn_chgQuantity.place(x=2, y=40)
        self.btn_discount.place(x=2, y=73)
        self.btn_tax.place(x=2, y=106)
        self.btn_remItem.place(x=2, y=139)
        self.btn_redeempts.place(x=2, y=172)
        self.btn_member.place(x=2, y=205)
        self.btn_exit.place(x=2, y=238)

        print("constructor called for sales ")
        self.sales_inventory_item(master)

    def sales_inventory_item(self, master):
        self.dataSearchFrame.destroy()
        self.dataSearchFrame = Frame(self.sales_window, width=1140, height=400, bd=2, relief='ridge',
                                     bg='snow')
        self.dataSearchFrame.pack()
        self.frameProductSearch = Frame(self.sales_window, width=1290, height=240, bd=2, relief='ridge',
                                        bg='snow')
        self.frameProductSearch.pack()
        frameSearch = Frame(self.dataSearchFrame, width=520, height=50, bd=2, relief='ridge',
                            bg='snow')
        frameSearch.pack()
        framedisplay = Frame(self.dataSearchFrame, width=520, height=195, bd=2, relief='ridge',
                             bg='snow')
        framedisplay.pack()

        framepurchase = Frame(self.dataSearchFrame, width=520, height=170, bd=2, relief='ridge',
                              bg='snow')
        framepurchase.pack()
        btn_search = Button(frameSearch)
        btn_search.configure(text="Search", fg="Black",
                             font=('arial narrow', 12, 'normal'), width=8, state=NORMAL, bg='RosyBrown1')
        btn_search.place(x=280, y=2)

        # designing a upper frame --------------------start----------------------------

        sales_label = Label(self.frameupper, text="Sales Login", width=9, anchor=W, justify=LEFT,
                            font=NORM_FONT,
                            bg='snow')
        sales_login = CurrentUser.get_instance().getCurrentUser()
        sales_txtlabel = Label(self.frameupper, width=15, text=sales_login, anchor=W, justify=LEFT,
                               font=NORM_FONT,
                               bg='light cyan')

        now = datetime.now()
        timeinfo = now.strftime("%H:%M")
        date_info = now.strftime("%d-%b-%Y")
        dateTimetxt = date_info + ',' + timeinfo
        dateTime_label = Label(self.frameupper, text="Date,Time", width=9, anchor=W, justify=LEFT,
                               font=NORM_FONT,
                               bg='snow')
        dateTime_txtlabel = Label(self.frameupper, width=15, text=dateTimetxt, anchor=W, justify=LEFT,
                                  font=NORM_FONT,
                                  bg='light cyan')
        billNo_label = Label(self.frameupper, text="Bill No.", width=9, anchor=W, justify=LEFT,
                             font=NORM_FONT,
                             bg='snow')
        inv_id = self.generate_StockPurchase_invoiceID()
        billNo_txtlabel = Label(self.frameupper, width=15, text=str(inv_id), anchor=W, justify=LEFT,
                                font=NORM_FONT,
                                bg='light cyan')
        customerAcct_label = Label(self.frameupper, text="Shopper Act.", width=11, anchor=W, justify=LEFT,
                                   font=NORM_FONT,
                                   bg='snow')
        customerAcct_txtlabel = Label(self.frameupper, width=15, anchor=W, justify=LEFT,
                                      font=NORM_FONT,
                                      bg='light cyan')
        customerName_label = Label(self.frameupper, text="Cust. Name", width=12, anchor=W, justify=LEFT,
                                   font=NORM_FONT,
                                   bg='snow')
        customerName_txt = Entry(self.frameupper, width=20, font=NORM_FONT, bg='light cyan')

        customercontact_label = Label(self.frameupper, text="Contact No.", width=10, anchor=W, justify=LEFT,
                                      font=NORM_FONT,
                                      bg='snow')
        self.customerContact_txt = Entry(self.frameupper, width=20, font=NORM_FONT, bg='light cyan')

        customerAddress_label = Label(self.frameupper, text="Address", width=10, anchor=W, justify=LEFT,
                                      font=NORM_FONT,
                                      bg='snow')
        customerAddress_txt = Entry(self.frameupper, width=28, font=NORM_FONT, bg='light cyan')
        framebtn = Frame(self.frameupper, width=327, height=40, bd=2, relief='ridge',
                         bg='snow')

        deatils_result = partial(self.displayCustomerDetails, self.customerContact_txt, customerName_txt,
                                 customerAddress_txt,
                                 customerAcct_txtlabel)
        fetchDetails_btn = Button(framebtn, text="Shopper Details", fg="Black", font=NORM_FONT, width=17, state=NORMAL,
                                  bg='RosyBrown1', command=deatils_result)
        resetCustDeatils_btn = Button(framebtn, text="Reset Shopper", fg="Black", font=NORM_FONT, width=17,
                                      state=NORMAL,
                                      bg='RosyBrown1')

        self.frameupper.place(x=155, y=5)
        sales_label.place(x=5, y=10)
        sales_txtlabel.place(x=100, y=10)
        dateTime_label.place(x=5, y=50)
        dateTime_txtlabel.place(x=100, y=50)

        billNo_label.place(x=250, y=10)
        billNo_txtlabel.place(x=350, y=10)
        customerAcct_label.place(x=250, y=50)
        customerAcct_txtlabel.place(x=350, y=50)

        customerName_label.place(x=500, y=10)
        customerName_txt.place(x=600, y=10)
        customercontact_label.place(x=500, y=50)
        self.customerContact_txt.place(x=600, y=50)

        customerAddress_label.place(x=800, y=10)
        customerAddress_txt.place(x=870, y=10)

        framebtn.place(x=800, y=40)
        fetchDetails_btn.place(x=1, y=1)
        resetCustDeatils_btn.place(x=160, y=1)
        # designing a upper frame --------------------end----------------------------

        item_SearchId = Label(frameSearch, text="Search Item Id", width=11, anchor=W, justify=LEFT,
                              font=NORM_FONT,
                              bg='snow')

        item_namelabel = Label(framedisplay, text="Item Name", width=10, anchor=W, justify=LEFT,
                               font=NORM_FONT,
                               bg='snow')

        author = Label(framedisplay, text="Author", width=10, anchor=W, justify=LEFT,
                       font=NORM_FONT,
                       bg='snow')

        price = Label(framedisplay, text="Price(Rs.)", width=12, anchor=W, justify=LEFT,
                      font=NORM_FONT, bg='snow')

        quantity = Label(framedisplay, text="Quantity", width=12, anchor=W, justify=LEFT,
                         font=NORM_FONT, bg='snow')

        purchase_quantitylbl = Label(framedisplay, text="Purchase Quantity", width=15, justify=CENTER,
                                     font=XL_FONT, bg='light green')
        quantity_entry = Entry(framedisplay, width=5, font=XL_FONT, bg='light cyan')
        quantity_entry.insert(0, "0")

        purchase_headline = Label(framepurchase, text="Bill Summary", width=13, anchor=W, justify=LEFT,
                                  font=NORM_FONT, bg='snow', fg='red')

        purchase_cartCountlbl = Label(framepurchase, text="Cart Count", width=13, anchor=W, justify=LEFT,
                                      font=NORM_FONT, bg='snow')
        purchase_moplbl = Label(framepurchase, text="Pts. Redeemed", width=13, anchor=W, justify=LEFT,
                                font=NORM_FONT, bg='snow')
        purchase_pointsEarnedlbl = Label(framepurchase, text="Pts. Earned", width=13, anchor=W, justify=LEFT,
                                         font=NORM_FONT, bg='snow')
        purchase_rempointslbl = Label(framepurchase, text="Rem. Points", width=13, anchor=W, justify=LEFT,
                                      font=NORM_FONT, bg='snow')
        # declaring remining points here to populate as ssoon as shopper details are fetched
        self.remPoints_text = Label(framepurchase, width=12, anchor=W, justify=LEFT,
                                    font=NORM_FONT,
                                    bg='light cyan')
        cartCount_text = Label(framepurchase, width=12, text="0", anchor=W, justify=LEFT,
                               font=NORM_FONT,
                               bg='light cyan')

        self.mop_text = Label(framepurchase, width=12, text="0", anchor=W, justify=LEFT,
                              font=NORM_FONT,
                              bg='light cyan')
        self.pointsEarned_text = Label(framepurchase, width=12, anchor=W, justify=LEFT,
                                       font=NORM_FONT,
                                       bg='light cyan')
        purchase_billAmtlbl = Label(framepurchase, text="Bill Amt.(Rs.)", width=13, anchor=W, justify=LEFT,
                                    font=NORM_FONT, bg='snow')
        self.billAmount_text = Label(framepurchase, width=13, anchor=W, justify=LEFT,
                                     font=NORM_FONT,
                                     bg='light cyan')
        purchase_discountlbl = Label(framepurchase, text="Discount(Rs.)", width=14, anchor=W, justify=LEFT,
                                     font=NORM_FONT, bg='snow')
        self.billdiscount_text = Label(framepurchase, width=13, anchor=W, text="0", justify=LEFT,
                                       font=NORM_FONT,
                                       bg='light cyan')
        purchase_taxlbl = Label(framepurchase, text="Tax %", width=14, anchor=W, justify=LEFT,
                                font=NORM_FONT, bg='snow')

        self.billtax_text = Label(framepurchase, width=13, anchor=W, text="0", justify=LEFT,
                                  font=NORM_FONT,
                                  bg='light cyan')
        purchase_finalBillAmtlbl = Label(framepurchase, text="Amt. Payable(Rs.)", width=14, anchor=W, justify=LEFT,
                                         font=NORM_FONT, bg='snow')
        self.finalBillAmt_text = Label(framepurchase, width=13, anchor=W, justify=LEFT,
                                       font=NORM_FONT,
                                       bg='light cyan')

        self.dataSearchFrame.place(x=155, y=105)
        frameSearch.place(x=5, y=5)
        framedisplay.place(x=5, y=60)
        framepurchase.place(x=5, y=220)

        item_SearchId.place(x=10, y=5)

        item_namelabel.place(x=10, y=5)
        author.place(x=10, y=40)
        price.place(x=10, y=80)
        quantity.place(x=200, y=80)
        purchase_quantitylbl.place(x=10, y=115)

        item_idforSearch = Entry(frameSearch, width=15, font=L_FONT, bg='light cyan')
        item_idforSearch.focus_set()
        item_name = Label(framedisplay, width=25, anchor=W, justify=LEFT,
                          font=NORM_FONT,
                          bg='light cyan')

        author_menu = Label(framedisplay, width=25, anchor=W, justify=LEFT,
                            font=NORM_FONT,
                            bg='light cyan')

        item_price = Label(framedisplay, width=8, anchor=W, justify=LEFT,
                           font=NORM_FONT,
                           bg='light cyan')

        item_quantity = Label(framedisplay, width=8, anchor=W, justify=LEFT,
                              font=NORM_FONT,
                              bg='light cyan')
        item_borrowfee = Label(framedisplay, width=25, anchor=W, justify=LEFT,
                               font=NORM_FONT,
                               bg='light cyan')
        localcenter_menu = Label(framedisplay, width=25, anchor=W, justify=LEFT,
                                 font=NORM_FONT,
                                 bg='light cyan')
        item_idforSearch.place(x=120, y=5)
        item_name.place(x=120, y=5)
        author_menu.place(x=120, y=40)
        item_price.place(x=120, y=80)
        item_quantity.place(x=272, y=80)
        quantity_entry.place(x=272, y=115)
        item_borrowfee.place(x=120, y=160)
        localcenter_menu.place(x=120, y=235)

        purchase_headline.place(x=10, y=5)
        purchase_cartCountlbl.place(x=10, y=35)
        cartCount_text.place(x=120, y=35)
        purchase_moplbl.place(x=10, y=140)
        self.mop_text.place(x=120, y=140)
        purchase_pointsEarnedlbl.place(x=10, y=105)
        self.pointsEarned_text.place(x=120, y=105)
        purchase_rempointslbl.place(x=10, y=70)
        self.remPoints_text.place(x=120, y=70)

        purchase_billAmtlbl.place(x=250, y=35)
        self.billAmount_text.place(x=385, y=35)
        purchase_discountlbl.place(x=250, y=70)
        self.billdiscount_text.place(x=385, y=70)
        purchase_taxlbl.place(x=250, y=105)
        self.billtax_text.place(x=385, y=105)
        purchase_finalBillAmtlbl.place(x=250, y=140)
        self.finalBillAmt_text.place(x=385, y=140)

        search_result = partial(self.search_itemId, item_idforSearch, item_name, author_menu,
                                item_price,
                                item_borrowfee,
                                item_quantity, quantity_entry, OPERATION_SEARCH)

        btn_search.configure(command=search_result)
        addToCart_result = partial(self.addToCart, item_idforSearch, item_name, quantity_entry, item_price,
                                   cartCount_text, self.billAmount_text)
        self.btn_addToCart.configure(command=addToCart_result)

        purchase_result = partial(self.tender_display)

        self.btn_submit.configure(command=purchase_result)
        self.btn_submit.configure(state=DISABLED, bg='light grey')

        reset_result = partial(self.reset_sales_frm, item_idforSearch, quantity_entry, customerName_txt,
                               self.customerContact_txt,
                               customerAddress_txt, item_name, author_menu,
                               item_price,
                               item_borrowfee,
                               item_quantity, )
        self.btn_reset.configure(command=reset_result)

        # Design of the search bottom area for products  -  start
        self.frameProductSearch.place(x=5, y=506)
        product_SearchIdlbl = Label(self.frameProductSearch, text="Barcode/Item Id", width=15, anchor=W, justify=LEFT,
                                    font=XL_FONT,
                                    bg='snow')
        product_SearchIdTxt = Entry(self.frameProductSearch, width=25, font=XL_FONT, bg='light cyan')
        product_namelbl = Label(self.frameProductSearch, text="Product Name", width=15, anchor=W, justify=LEFT,
                                font=XL_FONT,
                                bg='snow')
        product_NameTxt = Entry(self.frameProductSearch, width=25, font=XL_FONT, bg='light cyan')
        product_searchResult = partial(self.display_productDeatils, product_SearchIdTxt, product_NameTxt)
        btn_productSearch = Button(self.frameProductSearch, text="Search Item/s", fg="Black", font=NORM_FONT, width=17,
                                   state=NORMAL,
                                   bg='RosyBrown1', command=product_searchResult)
        product_SearchIdlbl.place(x=5, y=5)
        product_SearchIdTxt.place(x=200, y=5)
        product_namelbl.place(x=570, y=5)
        product_NameTxt.place(x=750, y=5)
        btn_productSearch.place(x=1110, y=5)

        self.display_SearchProductsDetailArea(self.frameProductSearch, 2, 45, 1260, 182)
        # Design of the search bottom area for products  -  end

        self.sales_window.bind('<Return>', lambda event=None: btn_search.invoke())
        self.sales_window.bind('<F1>', lambda event=None: self.btn_addToCart.invoke())
        self.sales_window.bind('<Alt-b>', lambda event=None: self.btn_submit.invoke())
        self.sales_window.bind('<Escape>', lambda event=None: self.btn_exit.invoke())
        self.sales_window.bind('<Alt-r>', lambda event=None: self.btn_reset.invoke())
        self.sales_window.bind('<Alt-p>', lambda event=None: self.btn_reset.invoke())
        # self.initialize_billArea()
        self.display_billArea(self.dataSearchFrame, 532, 5, 575, 378,BILL_NONE)
        self.sales_window.focus()
        self.sales_window.grab_set()
        mainloop()

    def reset_sales_frm(self, item_idforSearch, quantity_entry, name_entry, contact_entry, address_entry, item_name,
                        author_menu,
                        item_price,
                        item_borrowfee,
                        item_quantity, ):
        """ reset the text entry data on the sales form"""
        item_idforSearch.delete(0, END)
        item_idforSearch.configure(fg='black')
        quantity_entry.delete(0, END)
        quantity_entry.configure(fg='black')
        name_entry.delete(0, END)
        name_entry.configure(fg='black')
        contact_entry.delete(0, END)
        contact_entry.configure(fg='black')
        address_entry.delete(0, END)
        address_entry.configure(fg='black')
        item_name['text'] = ""
        author_menu['text'] = ""
        item_price['text'] = ""
        item_borrowfee['text'] = ""
        item_quantity['text'] = ""

    def display_billArea(self, split_open_window, startx, starty, xwidth, xheight,bill_type):
        self.billAreaFrame.destroy()
        self.billAreaFrame = Frame(split_open_window, relief=GROOVE, width=520, height=407, bd=2)
        self.billAreaFrame.place(x=startx, y=starty)

        mycanvas = Canvas(self.billAreaFrame)
        frame = Frame(mycanvas, width=200, height=100, bg='light yellow')
        myscrollbar = Scrollbar(self.billAreaFrame, orient="vertical", command=mycanvas.yview)
        mycanvas.configure(yscrollcommand=myscrollbar.set)

        myscrollbar.pack(side="right", fill="y")
        mycanvas.pack(side="left")
        mycanvas.create_window((0, 0), window=frame, anchor='nw')

        result = partial(self.myfunction, xwidth, xheight, mycanvas)

        frame.bind("<Configure>", result)

        label_Sno = Label(frame, text="S.No", width=4, height=1, anchor='center',
                          justify=CENTER,
                          font=('times new roman', 13, 'normal'),
                          bg='light yellow')

        label_detail2 = Label(frame, text="Item Name", width=28, height=1, anchor='center',
                              justify=CENTER,
                              font=('times new roman', 13, 'normal'),
                              bg='light yellow')

        label_detail3 = Label(frame, text="MRP(Rs.)", width=8, height=1,
                              anchor='center',
                              justify=CENTER,
                              font=('times new roman', 13, 'normal'),
                              bg='light yellow')

        label_detail4 = Label(frame, text="Quantity", width=8, height=1,
                              anchor='center',
                              justify=CENTER,
                              font=('times new roman', 13, 'normal'),
                              bg='light yellow')
        label_detail5 = Label(frame, text="Tot. Amt.(Rs.)", width=10, height=1,
                              anchor='center',
                              justify=CENTER,
                              font=('times new roman', 13, 'normal'),
                              bg='light yellow')

        label_Sno.grid(row=0, column=1, padx=2, pady=5)
        label_detail2.grid(row=0, column=2, padx=2, pady=5)
        label_detail3.grid(row=0, column=3, padx=2, pady=5)
        label_detail4.grid(row=0, column=4, padx=2, pady=5)
        label_detail5.grid(row=0, column=5, padx=2, pady=5)

        for row_index in range(0, len(self.list_InvoicePrint)):
            for column_index in range(1, 6):
                if column_index == 4:
                    width_column = 10
                elif column_index == 2:
                    width_column = 32
                elif column_index == 1:
                    width_column = 5
                elif column_index == 5:
                    width_column = 12
                elif column_index == 3:
                    width_column = 10
                else:
                    pass

                label_detail = Label(frame, text="No Data", width=width_column, height=1,
                                     anchor='center', justify=LEFT, bd=1,
                                     font=('arial narrow', 13, 'normal'),
                                     bg="light cyan")
                label_detail.grid(row=row_index + 1, column=column_index, padx=2, pady=1, sticky=W)

                if column_index == 1:
                    label_detail['text'] = str(row_index + 1)
                elif column_index == 2:
                    label_detail['text'] = self.list_InvoicePrint[row_index][1]
                elif column_index == 3:
                    label_detail['text'] = round(float(self.list_InvoicePrint[row_index][3]), 2)
                elif column_index == 4:
                    label_detail['text'] = self.list_InvoicePrint[row_index][2]
                elif column_index == 5:
                    label_detail['text'] = round((int(self.list_InvoicePrint[row_index][2]) * float(
                        self.list_InvoicePrint[row_index][3])), 2)
                else:
                    print("this value doesn't exists")
        self.calculateAndDisplayTotalBillAmt(bill_type)

    def display_SearchProductsDetailArea(self, split_open_window, startx, starty, xwidth, xheight):
        self.searchproductDeatilsArea.destroy()
        self.searchproductDeatilsArea = Frame(split_open_window, relief=GROOVE, width=1290, height=150, bd=2)
        self.searchproductDeatilsArea.place(x=startx, y=starty)

        mycanvas = Canvas(self.searchproductDeatilsArea)
        frame = Frame(mycanvas, width=200, height=100, bg='light yellow')
        myscrollbar = Scrollbar(self.searchproductDeatilsArea, orient="vertical", command=mycanvas.yview)
        mycanvas.configure(yscrollcommand=myscrollbar.set)

        myscrollbar.pack(side="right", fill="y")
        mycanvas.pack(side="left")
        mycanvas.create_window((0, 0), window=frame, anchor='nw')

        result = partial(self.myfunction, xwidth, xheight, mycanvas)

        frame.bind("<Configure>", result)

        label_Sno = Label(frame, text="S.No", width=10, height=1, anchor='center',
                          justify=CENTER,
                          font=('times new roman', 13, 'normal'),
                          bg='light yellow', relief='ridge')

        label_barcode = Label(frame, text="Id/Barcode", width=13, height=1, anchor='center',
                              justify=CENTER,
                              font=('times new roman', 13, 'normal'),
                              bg='light yellow', relief='ridge')

        label_productName = Label(frame, text="Product Name", width=30, height=1, anchor='center',
                                  justify=CENTER,
                                  font=('times new roman', 13, 'normal'),
                                  bg='light yellow', relief='ridge')

        label_OwnerName = Label(frame, text="Manufacturer", width=30, height=1,
                                anchor='center',
                                justify=CENTER,
                                font=('times new roman', 13, 'normal'),
                                bg='light yellow', relief='ridge')

        label_unitMRP = Label(frame, text="Unit MRP(Rs.)", width=20, height=1,
                              anchor='center',
                              justify=CENTER,
                              font=('times new roman', 13, 'normal'),
                              bg='light yellow', relief='ridge')
        label_quantity = Label(frame, text="Quantity", width=15, height=1,
                               anchor='center',
                               justify=CENTER,
                               font=('times new roman', 13, 'normal'),
                               bg='light yellow', relief='ridge')
        label_atRack = Label(frame, text="At Rack", width=16, height=1,
                             anchor='center',
                             justify=CENTER,
                             font=('times new roman', 13, 'normal'),
                             bg='light yellow', relief='ridge')

        label_Sno.grid(row=0, column=1, padx=1, pady=1)
        label_barcode.grid(row=0, column=2, padx=1, pady=1)
        label_productName.grid(row=0, column=3, padx=1, pady=1)
        label_OwnerName.grid(row=0, column=4, padx=1, pady=1)
        label_unitMRP.grid(row=0, column=5, padx=1, pady=1)
        label_quantity.grid(row=0, column=6, padx=1, pady=1)
        label_atRack.grid(row=0, column=7, padx=1, pady=1)

        for row_index in range(0, len(self.list_productDetails)):
            for column_index in range(1, 8):
                if column_index == 1:
                    width_column = 10
                elif column_index == 2:
                    width_column = 13
                elif column_index == 3:
                    width_column = 30
                elif column_index == 4:
                    width_column = 30
                elif column_index == 5:
                    width_column = 20
                elif column_index == 6:
                    width_column = 15
                elif column_index == 7:
                    width_column = 16
                else:
                    pass

                label_detail = Label(frame, text="No Data", width=width_column, height=1,
                                     anchor='center', justify=LEFT, bd=1,
                                     font=('arial narrow', 13, 'normal'),
                                     bg='light yellow')
                label_detail.grid(row=row_index + 1, column=column_index, padx=2, pady=1, sticky=W)

                if column_index == 1:
                    label_detail['text'] = str(row_index + 1)
                elif column_index == 2:
                    label_detail['text'] = self.list_productDetails[row_index][0]
                elif column_index == 3:
                    label_detail['text'] = self.list_productDetails[row_index][1]
                elif column_index == 4:
                    label_detail['text'] = self.list_productDetails[row_index][2]
                elif column_index == 5:
                    label_detail['text'] = self.list_productDetails[row_index][3]
                elif column_index == 6:
                    label_detail['text'] = self.list_productDetails[row_index][4]
                elif column_index == 7:
                    label_detail['text'] = self.list_productDetails[row_index][5]
                else:
                    print("this value doesn't exists")
        # clear the products list once table is drawn
        self.list_productDetails = []

    def change_quantity_display(self):
        change_quantity_window = Toplevel(self.dataSearchFrame)
        change_quantity_window.title("Change Quantity")
        change_quantity_window.geometry('320x150+950+380')
        change_quantity_window.configure(background='wheat')
        change_quantity_window.resizable(width=False, height=False)
        change_quantity_window.protocol('WM_DELETE_WINDOW', self.obj_commonUtil.donothing)

        label_itemSerialNo = Label(change_quantity_window, text="Bill S.No.", width=7, height=1, anchor=W, justify=LEFT,
                                   font=NORM_FONT,
                                   bg='wheat')
        sno_entry = Entry(change_quantity_window, width=15, font=NORM_FONT, bg='light cyan')

        label_quantity = Label(change_quantity_window, text="Quantity", width=7, height=1, anchor=W, justify=LEFT,
                               font=NORM_FONT,
                               bg='wheat')
        quantity_entry = Entry(change_quantity_window, width=15, font=NORM_FONT, bg='light cyan')
        btn_frame = Frame(change_quantity_window, width=230, height=50, bd=2, relief='ridge',
                          bg='purple')
        btn_changeQuantity = Button(btn_frame)
        change_result = partial(self.change_quantity, sno_entry, quantity_entry, change_quantity_window)
        btn_changeQuantity.configure(text="Change", fg="Black", font=NORM_FONT, width=9, state=NORMAL,
                                     bg='RosyBrown1', command=change_result)
        btn_printQuantity = Button(btn_frame)
        btn_printQuantity.configure(text="Cancel", fg="Black", font=NORM_FONT, width=9, state=NORMAL,
                                    bg='RosyBrown1', command=change_quantity_window.destroy)

        label_itemSerialNo.place(x=30, y=20)
        sno_entry.place(x=130, y=20)
        label_quantity.place(x=30, y=55)
        quantity_entry.place(x=130, y=55)
        btn_frame.place(x=50, y=90)
        btn_changeQuantity.place(x=3, y=2)
        btn_printQuantity.place(x=110, y=2)
        change_quantity_window.bind('<Return>', lambda event=None: btn_changeQuantity.invoke())
        change_quantity_window.bind('<Escape>', lambda event=None: btn_printQuantity.invoke())

    def discount_display(self):
        discount_display_window = Toplevel(self.dataSearchFrame)
        discount_display_window.title("Apply Discount")
        discount_display_window.geometry('300x135+950+380')
        discount_display_window.configure(background='wheat')
        discount_display_window.resizable(width=False, height=False)
        discount_display_window.protocol('WM_DELETE_WINDOW', self.obj_commonUtil.donothing)

        label_itemSerialNo = Label(discount_display_window, text="Bill S.No.", width=7, height=1, anchor=W,
                                   justify=LEFT,
                                   font=NORM_FONT,
                                   bg='wheat')
        sno_entry = Entry(discount_display_window, width=15, font=NORM_FONT, bg='light cyan')

        label_discount = Label(discount_display_window, text="Discount %", width=9, height=1, anchor=W, justify=LEFT,
                               font=NORM_FONT,
                               bg='wheat')
        discount_entry = Entry(discount_display_window, width=15, font=NORM_FONT, bg='light cyan')
        btn_frame = Frame(discount_display_window, width=185, height=40, bd=2, relief='ridge',
                          bg='purple')
        btn_changediscount = Button(btn_frame)
        change_result = partial(self.apply_discount, sno_entry, discount_entry, discount_display_window)
        btn_changediscount.configure(text="Apply", fg="Black", font=NORM_FONT, width=9, state=NORMAL,
                                     bg='RosyBrown1', command=change_result)
        btn_printdiscount = Button(btn_frame)
        btn_printdiscount.configure(text="Cancel", fg="Black", font=NORM_FONT, width=9, state=NORMAL,
                                    bg='RosyBrown1', command=discount_display_window.destroy)

        label_itemSerialNo.place(x=30, y=20)
        sno_entry.place(x=130, y=20)
        label_discount.place(x=30, y=55)
        discount_entry.place(x=130, y=55)
        btn_frame.place(x=50, y=90)
        btn_changediscount.place(x=1, y=2)
        btn_printdiscount.place(x=88, y=2)
        discount_display_window.bind('<Return>', lambda event=None: btn_changediscount.invoke())
        discount_display_window.bind('<Escape>', lambda event=None: btn_printdiscount.invoke())
        discount_display_window.focus()
        discount_display_window.grab_set()

    def customer_operations(self):
        objCustomer = Customer(self.sales_window)

    def tax_display(self):
        tax_display_window = Toplevel(self.dataSearchFrame)
        tax_display_window.title("Apply Tax %")
        tax_display_window.geometry('300x135+950+380')
        tax_display_window.configure(background='wheat')
        tax_display_window.resizable(width=False, height=False)
        tax_display_window.protocol('WM_DELETE_WINDOW', self.obj_commonUtil.donothing)

        label_itemSerialNo = Label(tax_display_window, text="Tax %", width=7, height=1, anchor=W,
                                   justify=LEFT,
                                   font=NORM_FONT,
                                   bg='wheat')
        taxAmt_entry = Entry(tax_display_window, width=15, font=NORM_FONT, bg='light cyan')

        label_tax = Label(tax_display_window, text="Amount(Rs.)", width=9, height=1, anchor=W, justify=LEFT,
                          font=NORM_FONT,
                          bg='wheat')
        tax_labelAmt = Label(tax_display_window, width=13, font=NORM_FONT, bg='light cyan', text='0')
        btn_frame = Frame(tax_display_window, width=185, height=40, bd=2, relief='ridge',
                          bg='purple')
        btn_applytax = Button(btn_frame)
        change_result = partial(self.apply_tax, taxAmt_entry)
        btn_applytax.configure(text="Apply", fg="Black", font=NORM_FONT, width=9, state=NORMAL,
                               bg='RosyBrown1', command=change_result)
        btn_close = Button(btn_frame)
        btn_close.configure(text="Cancel", fg="Black", font=NORM_FONT, width=9, state=NORMAL,
                            bg='RosyBrown1', command=tax_display_window.destroy)

        label_itemSerialNo.place(x=30, y=20)
        taxAmt_entry.place(x=130, y=20)
        label_tax.place(x=30, y=55)
        tax_labelAmt.place(x=130, y=55)
        btn_frame.place(x=50, y=90)
        btn_applytax.place(x=1, y=2)
        btn_close.place(x=88, y=2)

        tax_display_window.bind('<Return>', lambda event=None: btn_applytax.invoke())
        tax_display_window.bind('<Escape>', lambda event=None: btn_close.invoke())
        tax_display_window.focus()
        tax_display_window.grab_set()

    def sendEmail_display(self):
        sendEmail_display_window = Toplevel(self.dataSearchFrame)
        sendEmail_display_window.title("Send Email")
        sendEmail_display_window.geometry('300x135+950+380')
        sendEmail_display_window.configure(background='wheat')
        sendEmail_display_window.resizable(width=False, height=False)
        sendEmail_display_window.protocol('WM_DELETE_WINDOW', self.obj_commonUtil.donothing)

        label_itemSerialNo = Label(sendEmail_display_window, text="Email To:", width=7, height=1, anchor=W,
                                   justify=LEFT,
                                   font=NORM_FONT,
                                   bg='wheat')
        sendEmailTo_entry = Entry(sendEmail_display_window, width=15, font=NORM_FONT, bg='light cyan')

        btn_frame = Frame(sendEmail_display_window, width=185, height=40, bd=2, relief='ridge',
                          bg='purple')
        btn_applysendEmail = Button(btn_frame)
        change_result = partial(self.send_bill, sendEmailTo_entry, sendEmail_display_window)
        btn_applysendEmail.configure(text="Apply", fg="Black", font=NORM_FONT, width=9, state=NORMAL,
                                     bg='RosyBrown1', command=change_result)
        btn_close = Button(btn_frame)
        btn_close.configure(text="Cancel", fg="Black", font=NORM_FONT, width=9, state=NORMAL,
                            bg='RosyBrown1', command=sendEmail_display_window.destroy)

        label_itemSerialNo.place(x=30, y=20)
        sendEmailTo_entry.place(x=130, y=20)
        btn_frame.place(x=50, y=70)
        btn_applysendEmail.place(x=1, y=2)
        btn_close.place(x=88, y=2)

        sendEmail_display_window.bind('<Return>', lambda event=None: btn_applysendEmail.invoke())
        sendEmail_display_window.bind('<Escape>', lambda event=None: btn_close.invoke())
        sendEmail_display_window.focus()
        sendEmail_display_window.grab_set()

    def myfunction(self, xwidth, yheight, mycanvas, event):
        mycanvas.configure(scrollregion=mycanvas.bbox("all"), width=xwidth, height=yheight)

    def change_quantity(self, serialNo, newQuanity, change_quantity_window):
        print("Quantity change started for the serial no :", serialNo.get())
        bSerialValid = False
        for iLoop in range(0, len(self.list_InvoicePrint)):
            if iLoop + 1 == int(serialNo.get()):
                bSerialValid = True
                self.list_InvoicePrint[iLoop][2] = int(newQuanity.get())
                break

        if bSerialValid:
            print("Quantity has been changed")
            change_quantity_window.destroy()
            self.display_billArea(self.dataSearchFrame, 532, 5, 575, 378,BILL_NONE)
        else:
            print("Invalid Serial no")
            messagebox.showwarning("Invalid Quantity", "Check the serial no.")

    def removeItem_display(self):
        remItemt_display_window = Toplevel(self.dataSearchFrame)
        remItemt_display_window.title("Remove Item")
        remItemt_display_window.geometry('450x95+950+380')
        remItemt_display_window.configure(background='wheat')
        remItemt_display_window.resizable(width=False, height=False)
        remItemt_display_window.protocol('WM_DELETE_WINDOW', self.obj_commonUtil.donothing)

        label_itemSerialNo = Label(remItemt_display_window, text="Enter the item serial no. to remove :", width=30,
                                   height=1, anchor=W,
                                   justify=LEFT,
                                   font=NORM_FONT,
                                   bg='wheat')
        sno_entry = Entry(remItemt_display_window, width=15, font=NORM_FONT, bg='light cyan')
        sno_entry.focus_set()

        btn_frame = Frame(remItemt_display_window, width=225, height=40, bd=2, relief='ridge',
                          bg='purple')
        btn_remItem = Button(btn_frame)
        remove_result = partial(self.remove_item, sno_entry, remItemt_display_window)
        btn_remItem.configure(text="Remove", fg="Black", font=NORM_FONT, width=11, state=NORMAL,
                              bg='RosyBrown1', command=remove_result)
        btn_cancel = Button(btn_frame)
        btn_cancel.configure(text="Return", fg="Black", font=NORM_FONT, width=11, state=NORMAL,
                             bg='RosyBrown1', command=remItemt_display_window.destroy)

        label_itemSerialNo.place(x=20, y=20)
        sno_entry.place(x=280, y=20)
        btn_frame.place(x=100, y=50)
        btn_remItem.place(x=1, y=2)
        btn_cancel.place(x=110, y=2)
        remItemt_display_window.bind('<Return>', lambda event=None: btn_remItem.invoke())
        remItemt_display_window.bind('<Escape>', lambda event=None: btn_cancel.invoke())
        remItemt_display_window.focus()
        remItemt_display_window.grab_set()

    def redeemPoints_display(self):
        redeempts_display_window = Toplevel(self.dataSearchFrame)
        redeempts_display_window.title("Reedem points")
        redeempts_display_window.geometry('450x95+950+380')
        redeempts_display_window.configure(background='wheat')
        redeempts_display_window.resizable(width=False, height=False)
        redeempts_display_window.protocol('WM_DELETE_WINDOW', self.obj_commonUtil.donothing)

        label_ptsNo = Label(redeempts_display_window, text="Enter total points to redeem :", width=30, height=1,
                            anchor=W,
                            justify=LEFT,
                            font=NORM_FONT,
                            bg='wheat')
        points_entry = Entry(redeempts_display_window, width=15, font=NORM_FONT, bg='light cyan')
        points_entry.focus_set()

        btn_frame = Frame(redeempts_display_window, width=225, height=40, bd=2, relief='ridge',
                          bg='purple')
        btn_redeem = Button(btn_frame)
        remove_result = partial(self.reedem_points, points_entry, redeempts_display_window)
        btn_redeem.configure(text="Reedem", fg="Black", font=NORM_FONT, width=11, state=NORMAL,
                             bg='RosyBrown1', command=remove_result)
        btn_cancel = Button(btn_frame)
        btn_cancel.configure(text="Return", fg="Black", font=NORM_FONT, width=11, state=NORMAL,
                             bg='RosyBrown1', command=redeempts_display_window.destroy)

        label_ptsNo.place(x=20, y=20)
        points_entry.place(x=280, y=20)
        btn_frame.place(x=100, y=50)
        btn_redeem.place(x=1, y=2)
        btn_cancel.place(x=110, y=2)
        redeempts_display_window.bind('<Return>', lambda event=None: btn_redeem.invoke())
        redeempts_display_window.bind('<Escape>', lambda event=None: btn_cancel.invoke())
        redeempts_display_window.focus()
        redeempts_display_window.grab_set()

    def remove_item(self, serialNo, remitem_quantity_window):
        print("Remove Item  started for the serial no :", serialNo.get())
        bSerialValid = False
        for iLoop in range(0, len(self.list_InvoicePrint)):
            if iLoop + 1 == int(serialNo.get()):
                bSerialValid = True
                self.list_InvoicePrint.pop(int(serialNo.get()) - 1)
                # self.list_InvoicePrint[iLoop][2] = int(newQuanity.get())
                break

        if bSerialValid:
            print("Item has been removed form cart")
            remitem_quantity_window.destroy()
            self.display_billArea(self.dataSearchFrame, 532, 5, 575, 378,BILL_NONE)
        else:
            print("Invalid Serial no")
            messagebox.showwarning("Invalid Item", "Check the serial no.")

    def reedem_points(self, pointsToReedem, reedemPts_quantity_window):
        current_AvailablePts = self.getCurrentRedeemptionPoints()
        if float(current_AvailablePts) > float(pointsToReedem.get()) or float(current_AvailablePts) == float(
                pointsToReedem.get()):
            print("Redeem Points :", pointsToReedem.get())
            self.finalBillAmt_text['text'] = str(
                float(self.finalBillAmt_text.cget("text")) - float(pointsToReedem.get()))
            self.remPoints_text['text'] = str(round(float(current_AvailablePts) - int(pointsToReedem.get()), 1))
            self.mop_text["text"] = pointsToReedem.get()
        else:
            text_total = "Please try <" + str(current_AvailablePts)
            messagebox.showinfo("Ahh! Too much to en-cash", text_total)

    def apply_discount(self, serialNo, discountAmt, discount_window):
        print("Apply discount started for the serial no :", serialNo.get())
        bSerialValid = False

        for iLoop in range(0, len(self.list_InvoicePrint)):
            if iLoop + 1 == int(serialNo.get()):
                bSerialValid = True
                discounted_price = float((int(discountAmt.get()) / 100) * float(self.list_InvoicePrint[iLoop][3]))
                self.list_InvoicePrint[iLoop][3] = float(self.list_InvoicePrint[iLoop][3]) - discounted_price
                print("Discounted price is :", discounted_price)
                self.billdiscount_text['text'] = round(((discounted_price * int(
                    self.list_InvoicePrint[iLoop][2])) + float(self.billdiscount_text.cget("text"))), 2)
                break

        if bSerialValid:
            print("Quantity has been changed")
            discount_window.destroy()
            self.display_billArea(self.dataSearchFrame, 532, 5, 575, 378,DISCOUNT_TYPE)
        else:
            print("Invalid Serial no")
            messagebox.showwarning("Invalid Quantity", "Check the serial no.")

    def apply_tax(self, taxAmt_entry):
        print("Apply Tax% :", taxAmt_entry.get())
        total_bill_Amount = self.calculateTotalMRP()
        tax_amount = round(float((int(taxAmt_entry.get()) / 100) * total_bill_Amount), 2)
        self.billtax_text['text'] = str(tax_amount)
        self.btn_discount.configure(state=DISABLED, bg='light grey')
        self.calculateAndDisplayTotalBillAmt(TAX_TYPE)

    def addToCart(self, item_idforSearch, item_name, quantity_entry, item_price, cartCount_text, billAmount_text):
        print("Adding to Cart Item Id :", item_idforSearch.get())
        bItemExists = False
        # validate if item already exists in cart
        for iLoop in range(0, len(self.list_InvoicePrint)):
            if item_idforSearch.get() == self.list_InvoicePrint[iLoop][0]:
                print("Item Already exists in Cart")
                messagebox.showwarning("Duplicate Entry", "Item already in cart")
                bItemExists = True
        if not bItemExists:
            # check for valid quantity availability
            bValidQuantity = self.isQuantityValid(item_idforSearch.get(), quantity_entry.get())
            print("Valid Quantity :", bValidQuantity)
            if bValidQuantity and int(quantity_entry.get()) > 0:
                # prepare the cart locally and retain it as long as purchase button is pressed
                # this implementation list of array strategy to store the temporary cart items
                # cart items are flushed out once "Buy" event is executed
                arr_InvoiceRecords = [item_idforSearch.get(), item_name.cget("text"), quantity_entry.get(),
                                      int(item_price.cget("text"))]
                self.list_InvoicePrint.append(arr_InvoiceRecords)

                cartCount_text['text'] = str(len(self.list_InvoicePrint))

                # calculate the total mrp
                total_cart_mrp = 0
                for iLoop in range(0, len(self.list_InvoicePrint)):
                    total_cart_mrp = total_cart_mrp + (int(self.list_InvoicePrint[iLoop][2]) * int(
                        self.list_InvoicePrint[iLoop][3]))

                billAmount_text['text'] = str(total_cart_mrp)
                self.btn_submit.configure(state=NORMAL, bg='RosyBrown1')
                self.btn_resetCart.configure(state=NORMAL, bg='RosyBrown1')
                self.btn_tax.configure(state=NORMAL, bg='RosyBrown1')
                self.btn_chgQuantity.configure(state=NORMAL, bg='RosyBrown1')
                self.btn_remItem.configure(state=NORMAL, bg='RosyBrown1')
                self.btn_discount.configure(state=NORMAL, bg='RosyBrown1')
                self.btn_member.configure(state=NORMAL, bg='RosyBrown1')

                print("Added to Cart Item Id :", item_idforSearch.get())
                self.display_billArea(self.dataSearchFrame, 532, 5, 575, 378,BILL_NONE)
            else:
                if int(quantity_entry.get()) == 0:
                    messagebox.showwarning("Invalid Quantity !", "Purchase Quantity is Invalid")
                else:
                    messagebox.showwarning("Invalid Quantity !", "In-sufficient quantity for purchase")

    def purchase_stock_item(self):
        self.btn_addToCart.configure(state=DISABLED, bg='light grey')
        customer_details = self.getCustomerDetails(self.customerContact_txt)
        customer_name = customer_details[2]
        customer_contact = customer_details[3]
        customer_address = customer_details[4]
        print("Customer Name :", customer_name, "Contact :", customer_contact, "Address :",
              customer_address)
        libMemberId = "Not Available"
        dateTimeObj = date.today()
        dateOfPurchase = dateTimeObj.strftime("%Y-%m-%d ")
        # validate the member , if  already registered
        print(" Cart items :", self.list_InvoicePrint)
        invoice_id = self.generate_StockPurchase_invoiceID()
        # reading the cart and modifying the database with new quantity
        conn = sql_db.connect(user='root', host=SQL_SERVER, port=3306, database='inventorydb',password='password')
        for cartLoop in range(0, len(self.list_InvoicePrint)):
            print("Purchase step 1  -  Modifying Quantity of Item :", self.list_InvoicePrint[cartLoop][1])
            # Creating a cursor object using the cursor() method
            cursor = conn.cursor()
            current_stock_quantity = self.get_currentStockQuantity(self.list_InvoicePrint[cartLoop][0])
            new_quantity = current_stock_quantity - int(self.list_InvoicePrint[cartLoop][2])
            sql = "UPDATE inventory_stock set Quantity = %s where Item_Id = %s "
            values = (new_quantity, self.list_InvoicePrint[cartLoop][0])
            cursor.execute(sql, values)
            conn.commit()
        conn.close()

        self.btn_submit.configure(state=DISABLED, bg='light grey')
        self.btn_resetCart.configure(state=DISABLED, bg='light grey')
        self.btn_chgQuantity.configure(state=DISABLED, bg='light grey')
        self.btn_remItem.configure(state=DISABLED, bg='light grey')
        self.btn_tax.configure(state=DISABLED, bg='light grey')
        self.btn_discount.configure(state=DISABLED, bg='light grey')
        self.btn_redeempts.configure(state=DISABLED, bg='light grey')
        self.btn_member.configure(state=DISABLED, bg='light grey')

        # write the redemption points earned to database
        self.creditEarnedRedeemptionPoints(customer_contact)
        # generate Invoice
        self.generateInvoicePage(customer_name,
                                 libMemberId,
                                 dateOfPurchase,
                                 customer_contact,
                                 customer_address,
                                 invoice_id)
        self.list_InvoicePrint = []
        self.display_billArea(self.dataSearchFrame, 532, 5, 575, 378,BILL_NONE)

    def generateInvoicePage(self, customer_name,
                            libMemberId,
                            dateOfPurchase,
                            customer_contact,
                            customer_address,
                            invoice_id):

        print("Purchase Step 2 - Generating Invoice")
        # update the invoice database with invoice details

        file_name = "..\\Library_Stock\\Invoices\\Template\\sales-invoice.xlsx"
        # searchinfo_label.configure(text="Invoice is being generated. Please wait ...", fg="purple")
        wb_obj = openpyxl.load_workbook(file_name)
        sheet_obj = wb_obj.active

        sheet_obj.cell(row=10, column=1).value = "Address"
        sheet_obj.cell(row=11, column=1).value = customer_address
        sheet_obj.cell(row=12, column=1).value = "Pin-code : NA"

        sheet_obj.cell(row=2, column=6).value = dateOfPurchase
        sheet_obj.cell(row=3, column=6).value = invoice_id
        sheet_obj.cell(row=9, column=1).value = customer_name

        sheet_obj.cell(row=13, column=1).value = customer_contact

        sheet_obj.cell(row=16, column=1).value = "Admin"
        sheet_obj.cell(row=16, column=2).value = customer_name
        sheet_obj.cell(row=16, column=3).value = libMemberId
        sheet_obj.cell(row=16, column=4).value = customer_contact

        final_paymentValue = 0
        # clear the existing sales template
        for iLoop_row in range(0, 10):
            for iLoop_column in range(1, 7):
                sheet_obj.cell(row=19 + iLoop_row, column=iLoop_column).value = ""

        # filling the purchase details in invoice
        for iLoop in range(0, len(self.list_InvoicePrint)):
            tax = int(self.list_InvoicePrint[iLoop][2]) * (TAX_ON_MRP / 100)
            sheet_obj.cell(row=19 + iLoop, column=1).value = str(iLoop + 1)
            sheet_obj.cell(row=19 + iLoop, column=2).value = str(self.list_InvoicePrint[iLoop][1])  # Name
            sheet_obj.cell(row=19 + iLoop, column=3).value = str(self.list_InvoicePrint[iLoop][2])  # quantity
            sheet_obj.cell(row=19 + iLoop, column=4).value = str(self.list_InvoicePrint[iLoop][3])  # price of each item
            sheet_obj.cell(row=19 + iLoop, column=5).value = str(tax)
            sheet_obj.cell(row=19 + iLoop, column=6).value = str(
                ((int(self.list_InvoicePrint[iLoop][2])) * int(self.list_InvoicePrint[iLoop][3])) + int(tax))
            final_paymentValue = final_paymentValue + int(sheet_obj.cell(row=19 + iLoop, column=6).value)

        sheet_obj.cell(row=29, column=6).value = str(final_paymentValue)

        print("Invoice records  :")
        for iLoop in range(0, len(self.list_InvoicePrint)):
            print(" Record :", iLoop + 1, " :", self.list_InvoicePrint[iLoop][1])

        wb_obj.save(file_name)
        today = datetime.now()
        year = today.strftime("%Y")
        dirname = "..\\Library_Stock\\Invoices\\" + year
        if not os.path.exists(dirname):
            print("Current year directory is not available , hence building one")
            os.makedirs(dirname)
        dest_file = dirname + "\\" + invoice_id + ".pdf "

        self.obj_commonUtil.convertExcelToPdf(file_name, dest_file)

        self.btn_exit.configure(state=NORMAL, bg='RosyBrown1')
        print_result = partial(self.printInvoice, dest_file)
        self.btn_print.configure(state=NORMAL, bg='RosyBrown1', command=print_result)

        # disable to add to cart and purchase button, so that same invoice is not generated twice
        self.btn_submit.configure(state=DISABLED, bg='light grey')
        self.btn_addToCart.configure(state=DISABLED, bg='light grey')

        # update the invoice table
        self.updateInvoiceDatabase(invoice_id, dateOfPurchase, final_paymentValue, customer_name, customer_contact)
        # self.obj_commonUtil.clearSales_InvoiceData(file_name,len(self.list_InvoicePrint))

    def printInvoice(self, fileToPrint):
        os.startfile(fileToPrint, 'print')

    def resetcart(self):
        # Clear the cart since , purchase has happened .
        self.list_InvoicePrint = []

        # disable the button as they are no longer relevant with cart item count  = 0
        self.btn_submit.configure(state=DISABLED, bg='light grey')
        self.btn_print.configure(state=DISABLED, bg='light grey')
        self.btn_reset.configure(state=DISABLED, bg='light grey')
        self.btn_resetCart.configure(state=DISABLED, bg='light grey')

        self.display_billArea(self.dataSearchFrame, 532, 5, 575, 378,BILL_NONE)

    def updateInvoiceDatabase(self, invoice_id, dateOfPurchase, final_paymentValue, customer_name, customer_contact):
        conn = sql_db.connect(user='root', host=SQL_SERVER, port=3306, database='inventorydb',password='password')

        # Creating a cursor object using the cursor() method
        cursor = conn.cursor()
        total_records = cursor.execute("SELECT * FROM invoices")
        if total_records == 0:
            serial_no = 1
        else:
            serial_no = total_records + 1

        customername = customer_name
        customercontact = customer_contact
        sql = "INSERT INTO invoices VALUES(%s, %s, %s, %s, %s, %s)"
        values = (serial_no, invoice_id, dateOfPurchase, final_paymentValue, customername, customercontact)
        cursor.execute(sql, values)
        conn.commit()
        conn.close()

        logInfo = str(invoice_id) + " purchase" + " success"
        self.obj_commonUtil.logActivity(logInfo)

    def enable_PaymentMethodView(self, *args):
        print("Tracing  entry input")

        if self.default_text1.get() != "":
            self.tender_display()
        else:
            pass

    def tender_display(self):
        tender_window = Toplevel(self.dataSearchFrame)
        tender_window.title("Tender Screen")
        tender_window.geometry('760x250+700+300')
        tender_window.configure(background='white')
        tender_window.resizable(width=False, height=False)
        tender_window.protocol('WM_DELETE_WINDOW', self.obj_commonUtil.donothing)

        # -------Menu buttonframe start--------------------------
        mainMenuFrame = Frame(tender_window, width=153, height=240, bd=2, relief='ridge',
                              bg='wheat')
        mainmenu_label = Label(mainMenuFrame, text="Main Menu", width=12, justify=CENTER,
                               font=L_FONT,
                               bg='wheat')
        btn_done = Button(mainMenuFrame, text="Done", fg="Black", command=None,
                          font=L_FONT, width=12, state=NORMAL, bg='RosyBrown1')
        btn_tender = Button(mainMenuFrame, text="Tender Amt.", fg="Black", command=None,
                            font=L_FONT, width=12, state=DISABLED, bg='light grey')

        btn_billgen = Button(mainMenuFrame, text="Generate Bill", fg="Black", command=None,
                             font=L_FONT, width=12, state=DISABLED, bg='light grey')

        btn_printbill = Button(mainMenuFrame, text="Print Bill", fg="Black", command=None,
                               font=L_FONT, width=12, state=DISABLED, bg='light grey')

        btn_exittender = Button(mainMenuFrame, text="Exit", fg="Black", command=tender_window.destroy,
                                font=L_FONT, width=12, state=NORMAL, bg='RosyBrown1')
        # Side button panel - end
        mainMenuFrame.place(x=5, y=2)
        mainmenu_label.place(x=2, y=5)
        btn_done.place(x=4, y=37)
        btn_tender.place(x=4, y=77)
        btn_billgen.place(x=4, y=117)
        btn_printbill.place(x=4, y=157)
        btn_exittender.place(x=4, y=197)
        # -------Menu buttonframe end--------------------------

        frame_left = Frame(tender_window, width=300, height=240, bd=2, relief='ridge',
                           bg='papayawhip')
        headline_lbl = Label(frame_left, text="Tender Mode", width=19, height=1, justify=CENTER,
                             font=XL_FONT, bd=2, relief='ridge',
                             bg='paleturquoise')

        info_label = Label(frame_left, text="Enter the Service Tax(if applicable)\n and press Enter or Done", width=30,
                           height=2, justify=CENTER,
                           font=NORM_FONT, bd=1, fg='green',
                           bg='papayawhip')
        frame_leftInputMode = Frame(frame_left, width=290, height=150, relief='ridge',
                                    bg='papayawhip')

        tender_modeText = StringVar(frame_leftInputMode)
        modelist = ['Cash', 'Google Pay', 'Phone Pay', 'Paytm', 'UPI', 'Credit Card', 'Debit Card', 'Sodexo', 'Coupon',
                    'Bank Transfer']
        print("Payment Modes - ", modelist)
        tender_modeText.set(modelist[0])
        tenderMenu = OptionMenu(frame_leftInputMode, tender_modeText, *modelist)
        tenderMenu.configure(width=22, font=('times new roman', 17, 'normal'), bg='light cyan', justify=CENTER)
        tender_amtlbl = Label(frame_leftInputMode, text="Amount(Rs.)", width=12, height=1, anchor=W, justify=LEFT,
                              font=NORM_FONT,
                              bg='papayawhip')
        tender_amtTxt = Entry(frame_leftInputMode, width=15, font=NORM_FONT, bg='light cyan', justify=RIGHT)
        tender_amtTxt.insert(0, self.finalBillAmt_text.cget("text"))
        service_chargelbl = Label(frame_leftInputMode, text="Service Tax(%)", width=12, height=1, anchor=W,
                                  justify=LEFT,
                                  font=NORM_FONT,
                                  bg='papayawhip')
        servcie_chargeTxt = Entry(frame_leftInputMode, width=15, font=NORM_FONT, bg='light cyan',
                                  justify=RIGHT)
        servcie_chargeTxt.insert(0, "0")
        total_amtlbl = Label(frame_leftInputMode, text="Total Amount", width=12, height=1, anchor=W, justify=LEFT,
                             font=L_FONT,
                             bg='papayawhip')

        total_amtTxt = Label(frame_leftInputMode, width=12, font=L_FONT, bg='royalblue', fg="white", anchor=E,
                             justify=RIGHT)
        textAmt = (round(float(tender_amtTxt.get()) + float(servcie_chargeTxt.get()), 2))
        total_amtTxt["text"] = str(textAmt)

        frame_left.place(x=160, y=1)
        headline_lbl.place(x=2, y=1)
        info_label.place(x=2, y=195)
        frame_leftInputMode.place(x=4, y=45)
        tenderMenu.place(x=3, y=2)
        tender_amtlbl.place(x=2, y=50)
        tender_amtTxt.place(x=147, y=50)
        service_chargelbl.place(x=2, y=82)
        servcie_chargeTxt.place(x=147, y=82)
        total_amtlbl.place(x=2, y=114)
        total_amtTxt.place(x=147, y=114)

        frame_right = Frame(tender_window, width=293, height=240, bd=2, relief='ridge',
                            bg='papayawhip')
        frame_right_paymodes = Frame(frame_right, width=285, height=160, bd=2, relief='ridge',
                                     bg='papayawhip')
        summary_lbl = Label(frame_right_paymodes, text="Tender Summary", width=17, height=1, justify=LEFT, anchor=W,
                            font=L_FONT, bd=1, fg='green',
                            bg='papayawhip')
        billAmt_lbl = Label(frame_right_paymodes, text="Bill Amt.(Rs.)", width=12, height=1, justify=LEFT, anchor=W,
                            font=NORM_FONT, bd=1,
                            bg='papayawhip')
        svtax_lbl = Label(frame_right_paymodes, text="Service Tax(%)", width=12, height=1, justify=LEFT, anchor=W,
                          font=NORM_FONT, bd=1,
                          bg='papayawhip')
        paymtMode_lbl = Label(frame_right_paymodes, text="Paymt. Mode", width=12, height=1, justify=LEFT, anchor=W,
                              font=NORM_FONT, bd=1,
                              bg='papayawhip')
        grossbill_lbl = Label(frame_right_paymodes, text="Gross Amt.(Rs.)", width=12, height=1, justify=LEFT, anchor=W,
                              font=NORM_FONT, bd=1,
                              bg='papayawhip')
        received_lbl = Label(frame_right, text="Received(Rs.)", width=11, height=1, justify=LEFT, anchor=W,
                             font=L_FONT, bd=1,
                             bg='papayawhip')

        balance_lbl = Label(frame_right, text="Balance(Rs.)", width=11, height=1, justify=LEFT, anchor=W,
                            font=L_FONT, bd=1,
                            bg='papayawhip')

        billAmt_txt = Label(frame_right_paymodes, width=15, height=1, justify=LEFT, anchor=W,
                            font=NORM_FONT, bd=1,
                            bg='light cyan')
        serviceTax_txt = Label(frame_right_paymodes, width=15, height=1, justify=LEFT, anchor=W,
                               font=NORM_FONT, bd=1,
                               bg='light cyan')
        paymtMode_txt = Label(frame_right_paymodes, width=15, height=1, justify=LEFT, anchor=W,
                              font=NORM_FONT, bd=1,
                              bg='light cyan')
        grossbill_txt = Label(frame_right_paymodes, width=15, height=1, justify=LEFT, anchor=W,
                              font=NORM_FONT, bd=1,
                              bg='light cyan')
        received_txt = Entry(frame_right, width=8, text="0.0", font=L_FONT, bg='light grey', fg="white",
                             justify=CENTER, state=DISABLED)
        received_txt.insert(0, "0.0")
        balance_txt = Label(frame_right, width=6, height=1, justify=RIGHT, anchor=E,
                            font=L_FONT, bd=1, fg="green", text="0.0",
                            bg='papayawhip')
        tender_amtresult = partial(self.enablepayment, received_txt)
        btn_tender.configure(command=tender_amtresult)

        textAmt = (round(float(tender_amtTxt.get()) + float(servcie_chargeTxt.get()), 2))
        balance_txt["text"] = str(textAmt)

        frame_right.place(x=460, y=1)
        frame_right_paymodes.place(x=2, y=1)
        summary_lbl.place(x=2, y=2)
        billAmt_lbl.place(x=2, y=35)
        svtax_lbl.place(x=2, y=65)
        paymtMode_lbl.place(x=2, y=95)
        grossbill_lbl.place(x=2, y=125)
        received_lbl.place(x=2, y=165)
        balance_lbl.place(x=2, y=198)

        billAmt_txt.place(x=130, y=35)
        serviceTax_txt.place(x=130, y=65)
        paymtMode_txt.place(x=130, y=95)
        grossbill_txt.place(x=130, y=125)
        received_txt.place(x=170, y=165)
        balance_txt.place(x=170, y=198)

        tender_window.focus()
        tender_window.grab_set()

        done_result = partial(self.done_operations, servcie_chargeTxt, total_amtTxt, billAmt_txt, serviceTax_txt,
                              paymtMode_txt, grossbill_txt, balance_txt, tender_modeText, btn_tender, btn_billgen,
                              btn_printbill, info_label, received_txt)
        btn_done.configure(command=done_result)
        tender_window.bind('<Return>', lambda event=None: btn_done.invoke())
        tender_window.bind('<Escape>', lambda event=None: btn_exittender.invoke())

    def done_operations(self, servcie_chargeTxt, total_amtTxt, billAmt_txt, serviceTax_txt, paymtMode_txt,
                        grossbill_txt, balance_txt, tender_modeText, btn_tender, btn_billgen, btn_printbill,
                        info_label, received_txt):
        serviceChg_amt = (float(servcie_chargeTxt.get()) / 100) * float(self.finalBillAmt_text.cget("text"))
        gross_amount = round(serviceChg_amt + float(self.finalBillAmt_text.cget("text")), 2)
        if received_txt.get() == "":
            total_amtTxt["text"] = str(gross_amount)
            billAmt_txt["text"] = self.finalBillAmt_text.cget("text")
            serviceTax_txt["text"] = servcie_chargeTxt.get()
            paymtMode_txt["text"] = tender_modeText.get()
            grossbill_txt["text"] = str(gross_amount)
            received_txt.insert(0, "0.0")
            # balance is equal to gross amount , before payment is done
            balance_txt["text"] = str(gross_amount)
            # enabling the relevant buttons
            btn_tender.configure(state=NORMAL, bg='RosyBrown1')
            info_text = "Total Payment amount : " + str(gross_amount)
            info_label.configure(text=info_text)
            self.btn_discount.configure(state=DISABLED, bg="light grey")
            self.btn_tax.configure(state=DISABLED, bg="light grey")
            self.btn_remItem.configure(state=DISABLED, bg="light grey")
            self.btn_redeempts.configure(state=DISABLED, bg="light grey")
        else:
            # bill generate and print bill options shall be enabled and processed
            btn_billgen.configure(state=NORMAL, bg='RosyBrown1')
            btn_printbill.configure(state=NORMAL, bg='RosyBrown1')
            balance_txt["text"] = str(float(gross_amount) - float(received_txt.get()))

    def enablepayment(self, received_txt):
        received_txt.configure(state=NORMAL, bg='royalblue')

    def check_SaveItemBtn_state(self, *args):
        print("Tracing  entry input")
        if self.default_text1.get() != "" and \
                self.default_text3.get() != "" and \
                self.default_text4.get() != "" and \
                self.default_text5.get() != "":

            self.btn_submit.configure(state=NORMAL, bg='RosyBrown1')
        else:
            self.btn_submit.configure(state=DISABLED, bg='light grey')

    def calculateAndDisplayTotalBillAmt(self, bill_type):
        if bill_type == BILL_NONE:
            total_cart_mrp = self.calculateTotalMRP()
            self.billAmount_text['text'] = str(total_cart_mrp)

        self.finalBillAmt_text['text'] = str(
            float(self.billAmount_text.cget("text")) + float(self.billtax_text.cget("text"))-float(self.billdiscount_text.cget("text")))
        self.pointsEarned_text['text'] = str(float(self.finalBillAmt_text.cget("text")) / 100)

    def calculateTotalMRP(self):
        # calculate the total mrp
        total_cart_mrp = 0
        for iLoop in range(0, len(self.list_InvoicePrint)):
            total_cart_mrp = total_cart_mrp + round((int(self.list_InvoicePrint[iLoop][2]) * float(
                self.list_InvoicePrint[iLoop][3])), 2)
        return total_cart_mrp

    # Function for clearing the
    # contents of text entry boxes
    def clear_form(self, name, author, price, quantity, borrowFee):
        # clear the content of text entry box
        name.delete(0, END)
        name.configure(fg='black')
        price.delete(0, END)
        price.configure(fg='black')
        quantity.delete(0, END)
        quantity.configure(fg='black')
        borrowFee.delete(0, END)
        borrowFee.configure(fg='black')

    def stock_operations(self, sales_window, item_name, item_idforSearch, author_name, item_price, item_borrowfee,
                         item_quantity,
                         rack_location, cal, local_centerText, item_TypeText, op_type, receiver_name, order_id,
                         sender_name):

        dateTimeObj = cal.get_date()

        receival_date = dateTimeObj.strftime("%Y-%m-%d")
        if op_type == OPERATION_ADD:
            item_id = self.generate_itemId(local_centerText.get())  # generates a unique item id
        elif op_type == OPERATION_EDIT:
            item_id = item_idforSearch.get()
        if item_name.get() == "" or author_name.get() == "" or item_price.get() == "" or item_quantity.get() == "" or item_borrowfee.get() == "":
            messagebox.showinfo("Data Entry Error", "All fields are mandatory !!!")

        else:
            bitemExists = self.validate_itemName(item_name.get(), local_centerText.get())
            print("bitemExists :", bitemExists)
            if bitemExists and op_type is OPERATION_ADD:
                messagebox.showwarning("Duplicate Entry Error !", "Item already exists !!")
                item_name.configure(bd=2, fg='red')
                return
            else:
                conn = sql_db.connect(user='root', host=SQL_SERVER, port=3306, database='inventorydb',password='password')

                # Creating a cursor object using the cursor() method
                cursor = conn.cursor()
                total_records = cursor.execute("SELECT * FROM inventory_stock")
                conn.close()

                if total_records == 0:
                    serial_no = 1
                else:
                    serial_no = total_records + 1

                # establishing the connection
                print("debug 1")
                conn = sql_db.connect(user='root', host=SQL_SERVER, port=3306, database='inventorydb',password='password')
                print("debug 2")
                # Creating a cursor object using the cursor() method
                cursor = conn.cursor()
                print("debug 3")
                itemname = str(item_name.get())
                author = str(author_name.get())
                price = int(item_price.get())
                borrow_fee = int(item_borrowfee.get())
                quantity = int(item_quantity.get())
                location = rack_location.get()
                localcenter = local_centerText.get()
                stocktype = item_TypeText.get()
                receiver = receiver_name.get()
                orderid = order_id.get()
                sendername = sender_name.get()
                print("\n", serial_no, item_id, itemname, author, price, borrow_fee, quantity, location, receival_date,
                      localcenter, stocktype, stocktype, receiver, orderid, sendername)
                if op_type is OPERATION_ADD:
                    print("\n Add operation type")
                    sql = "INSERT INTO inventory_stock VALUES(%s, %s, %s, %s,%s, %s, %s, %s,%s, %s, %s,%s, %s, %s)"
                    values = (
                        serial_no, item_id, itemname, author, price, borrow_fee, quantity, location, receival_date,
                        localcenter, stocktype, receiver, orderid, sendername)
                    cursor.execute(sql, values)
                elif op_type is OPERATION_EDIT:
                    print("\n Edit operation type")
                    sql = "UPDATE inventory_stock set Item_name = %s, Author_Name = %s, Price = %s, Borrow_Fee = %s, " \
                          "Quantity = %s, Location = %s, Stock_Receival_Date = %s, Center_Name = %s, Stock_Type = %s " \
                          "where Item_Id = %s "
                    # sql = "UPDATE inventory_stock set Item_name = %s where Item_Id = %s"
                    values = (
                        itemname, author, price, borrow_fee, quantity, location, cal.get_date(), localcenter, stocktype,
                        item_id)
                    cursor.execute(sql, values)
                else:
                    '''do nothing'''

                # execute the query
                conn.commit()
                conn.close()
                print("Record inserted !!! ")

                self.btn_submit.configure(state=DISABLED, bg='light grey')
                self.clear_form(item_name, author_name, item_price, item_borrowfee, item_quantity)
                user_choice = messagebox.askquestion("Item insertion success", "Do you want to add another item ? ")
                # destroy the data entry form , if user do not want to add more records
                if user_choice == 'no':
                    print("Do nothing")

    def search_itemId(self, item_idforSearch, item_name, author_menu,
                      item_price,
                      item_author,
                      item_quantity, quantity_entry, op_type):

        # search started -------------
        print("search_itemId--> Start for item name: ", item_idforSearch.get())
        itemId = item_idforSearch.get()
        bItemExists = self.validate_itemId(itemId)
        if bItemExists:
            conn = sql_db.connect(user='root', host=SQL_SERVER, port=3306, database='inventorydb',password='password')

            # Creating a cursor object using the cursor() method
            cursor = conn.cursor()

            bItemExist = cursor.execute("SELECT * FROM inventory_stock WHERE Item_Id = %s", (itemId,))
            result = cursor.fetchone()
            print("result :", result)
            conn.close()
            if op_type == OPERATION_EDIT:
                item_name.delete(0, END)
                item_name.insert(0, result[2])
                item_price.delete(0, END)
                item_price.insert(0, result[4])
                item_author.delete(0, END)
                item_author.insert(0, result[3])
                item_quantity.delete(0, END)
                item_quantity.insert(0, result[6])
            elif op_type == OPERATION_SEARCH:
                item_name['text'] = result[2]
                author_menu['text'] = result[3]
                item_price['text'] = result[4]
                item_author['text'] = result[9]
                item_quantity['text'] = result[6]
                quantity_entry.focus_set()
            else:
                ''' do nothing '''
            self.btn_addToCart.configure(state=NORMAL, bg='RosyBrown1')
        else:
            messagebox.showwarning("Not Available", "Item doesn't exists!!!")

    def display_productDeatils(self, item_idforSearch, item_name):
        # search started -------------
        print("display_productDeatils--> Start for barcode/id: ", item_idforSearch.get(), "Name :", item_name.get())
        itemId = item_idforSearch.get()

        conn = sql_db.connect(user='root', host=SQL_SERVER, port=3306, database='inventorydb',password='password')
        bSearchValid = True
        # Creating a cursor object using the cursor() method
        cursor = conn.cursor()
        bSearchValid = True
        itemName = item_name.get()
        if item_name.get() != "" and item_idforSearch.get() != "":
            print("Case 1")
            bItemExist = cursor.execute("SELECT * FROM inventory_stock WHERE Item_Id =%s  Item_name=%s",
                                        (itemId, item_name.get()))
        elif item_name.get() != "" and item_idforSearch.get() == "":
            print("Case 2")
            bItemExist = cursor.execute("SELECT * FROM inventory_stock WHERE Item_name LIKE %s ",
                                        ("%" + itemName + "%",))
        elif item_name.get() == "" and item_idforSearch.get() != "":
            print("Case 3")
            bItemExist = cursor.execute("SELECT * FROM inventory_stock WHERE Item_Id = %s", (itemId,))
        else:
            bSearchValid = False

        if bSearchValid:
            result = cursor.fetchall()
            print("display_productDetails result : \n", result)
            for iLoop in range(0, len(result)):
                arr_productDetails = [result[iLoop][1], result[iLoop][2], result[iLoop][3], result[iLoop][4],
                                      result[iLoop][6], result[iLoop][7]]
                self.list_productDetails.append(arr_productDetails)
            conn.close()
            self.display_SearchProductsDetailArea(self.frameProductSearch, 2, 45, 1260, 182)
        else:
            messagebox.showwarning("Not Available", "Item doesn't exists!!!")

    def generate_itemId(self):
        conn = sql_db.connect(user='root', host=SQL_SERVER, port=3306, database='inventorydb',password='password')

        # Creating a cursor object using the cursor() method
        cursor = conn.cursor()
        total_records = cursor.execute("SELECT * FROM inventory_stock")
        conn.close()
        stock_id = total_records + 100
        return "INV" + str(stock_id)  # CI- Commercial Inventory

    def validate_itemName(self, itemName, localCenterName):
        itemId = ""
        print("validate_itemName--> Start for item name: ", itemName)
        conn = sql_db.connect(user='root', host=SQL_SERVER, port=3306, database='inventorydb',password='password')

        # Creating a cursor object using the cursor() method
        cursor = conn.cursor()

        bItemExist = cursor.execute("SELECT EXISTS(SELECT * FROM inventory_stock WHERE Item_name = %s)", (itemName,))
        result = cursor.fetchone()
        print("result :", result[0])
        conn.close()
        return result[0]

    def isQuantityValid(self, itemdId, quantity_requested):
        print("isQuantityValid--> Start for item id: ", itemdId)
        b_QuantityValid = True
        conn = sql_db.connect(user='root', host=SQL_SERVER, port=3306, database='inventorydb',password='password')

        # Creating a cursor object using the cursor() method
        cursor = conn.cursor()

        bItemExist = cursor.execute("SELECT Quantity FROM inventory_stock WHERE Item_Id = %s", (itemdId,))

        result = cursor.fetchone()
        print("result of item_id:", result[0])
        conn.close()
        if int(result[0]) < int(quantity_requested):
            b_QuantityValid = False
        return b_QuantityValid

    def validate_itemId(self, itemId):
        print("validate_itemId--> Start for item Id : ", itemId)
        conn = sql_db.connect(user='root', host=SQL_SERVER, port=3306, database='inventorydb',password='password')

        # Creating a cursor object using the cursor() method
        cursor = conn.cursor()

        bItemExist = cursor.execute("SELECT EXISTS(SELECT * FROM inventory_stock WHERE Item_Id = %s)", (itemId,))
        result = cursor.fetchone()
        print("result of item_id:", result[0])
        conn.close()
        return result[0]

    def generate_authorId(self):
        conn = sql_db.connect(user='root', host=SQL_SERVER, port=3306, database='inventorydb',password='password')

        # Creating a cursor object using the cursor() method
        cursor = conn.cursor()
        total_records = cursor.execute("SELECT * FROM author")
        conn.close()
        authorId = total_records + 100
        return "ATH" + str(authorId)  # Author Id

    def validate_author(self, name_text):
        print("validate_author--> validate for Name : ", name_text)
        conn = sql_db.connect(user='root', host=SQL_SERVER, port=3306, database='inventorydb',password='password')

        # Creating a cursor object using the cursor() method
        cursor = conn.cursor()

        bItemExist = cursor.execute("SELECT EXISTS(SELECT * FROM author WHERE author_Name = %s)", (name_text,))
        result = cursor.fetchone()
        print("result :", result[0])
        conn.close()
        return result[0]

    def get_centerNames(self):
        # establishing the database connection
        conn = sql_db.connect(user='root', host=SQL_SERVER, port=3306, database='inventorydb',password='password')

        # Creating a cursor object using the cursor() method
        cursor = conn.cursor()

        result_query = cursor.execute("SELECT merchandise_Name FROM merchandise")

        # fetching all results from the executed query
        result = cursor.fetchall()

        # closing the connection
        conn.close()

        # return the result
        return result

    def generate_StockPurchase_invoiceID(self):
        conn = sql_db.connect(user='root', host=SQL_SERVER, port=3306, database='inventorydb',password='password')

        # Creating a cursor object using the cursor() method
        cursor = conn.cursor()
        total_records = cursor.execute("SELECT * FROM invoices")
        bItemExist = cursor.execute("select invoice_id from invoices ORDER BY invoice_id DESC LIMIT 1 ")
        last_invId = cursor.fetchone()
        print("Last invoice id :", last_invId)
        if total_records > 0:
            finalId = int(last_invId[0]) + 1
        else:
            finalId = 1
        print("Generated Invoice Id : ", finalId)
        conn.close()
        return str(finalId)

    def get_currentStockQuantity(self, item_id):
        conn = sql_db.connect(user='root', host=SQL_SERVER, port=3306, database='inventorydb',password='password')

        # Creating a cursor object using the cursor() method
        cursor = conn.cursor()

        bItemExist = cursor.execute("SELECT Quantity FROM inventory_stock WHERE Item_Id = %s", (item_id,))
        result = cursor.fetchone()
        print("Current quantity :", result)
        conn.close()
        return int(result[0])

    def displayCustomerDetails(self, customerContact_txt, customerName_txt, customerAddress_txt, customerAcct_txtlabel):
        conn = sql_db.connect(user='root', host=SQL_SERVER, port=3306, database='inventorydb',password='password')

        # Creating a cursor object using the cursor() method
        cursor = conn.cursor()
        if self.customerContact_txt.get() != "":
            bItemExist = cursor.execute("SELECT * FROM customer_details WHERE customer_contact = %s",
                                        (self.customerContact_txt.get(),))
            result = cursor.fetchone()
            print("result :", result)
            if result is not None:
                customerName_txt.delete(0, END)
                customerName_txt.insert(0, result[2])  # name
                customerAddress_txt.delete(0, END)
                customerAddress_txt.insert(0, result[4])  # address
                customerAcct_txtlabel['text'] = result[1]  # account number
                self.remPoints_text['text'] = self.getCurrentRedeemptionPoints()
                if float(self.getCurrentRedeemptionPoints()) > 0:
                    self.btn_redeempts.configure(state=NORMAL, bg='RosyBrown1')
            else:
                messagebox.showwarning("Invalid Data", "Ahh, This contact is not registered")
                self.btn_redeempts.configure(state=DISABLED, bg='light grey')
        else:
            messagebox.showwarning("No data", "OOPS! Contact No. is empty")
            self.btn_redeempts.configure(state=DISABLED, bg='light grey')
        conn.close()

    def getCustomerDetails(self, customerContact_txt):
        conn = sql_db.connect(user='root', host=SQL_SERVER, port=3306, database='inventorydb',password='password')

        # Creating a cursor object using the cursor() method
        cursor = conn.cursor()

        bItemExist = cursor.execute("SELECT * FROM customer_details WHERE customer_contact = %s",
                                    (customerContact_txt.get(),))
        result = cursor.fetchone()
        print("result :", result)
        conn.close()
        return result

    def creditEarnedRedeemptionPoints(self, customer_contact):
        """ earned points on purchase are written to database in individual accounts"""
        conn = sql_db.connect(user='root', host=SQL_SERVER, port=3306, database='inventorydb',password='password')

        # Creating a cursor object using the cursor() method
        cursor = conn.cursor()
        pointsEarned = self.pointsEarned_text.cget("text")
        print("Points earned :", pointsEarned, " writing to database")
        bItemExist = cursor.execute("SELECT customer_redeempoints FROM customer_details WHERE customer_contact = %s",
                                    (customer_contact,))
        result = cursor.fetchone()
        print("Existing Points :", str(result[0]))

        new_total_points = round((float(str(result[0])) + float(pointsEarned)), 2)
        print("New Total Points :", new_total_points)
        sql = "UPDATE customer_details set customer_redeempoints = %s where customer_contact = %s "
        values = (str(new_total_points), customer_contact.get())
        cursor.execute(sql, values)
        conn.commit()
        conn.close()

    def getCurrentRedeemptionPoints(self):
        """ earned points on purchase are written to database in individual accounts"""
        conn = sql_db.connect(user='root', host=SQL_SERVER, port=3306, database='inventorydb',password='password')

        # Creating a cursor object using the cursor() method
        cursor = conn.cursor()
        customer_contact = self.customerContact_txt.get()
        print("Customer contact :", customer_contact)
        # if customer contact is not empty
        if customer_contact != "":
            bItemExist = cursor.execute(
                "SELECT customer_redeempoints FROM customer_details WHERE customer_contact = %s",
                (customer_contact,))
            result = cursor.fetchone()
            print("Existing Points :", result)
            conn.close()
            return str(result[0])
        else:
            text_to_return = "0.0"
            return text_to_return

    def prepare_bill(self):
        pass

    def send_bill(self, sendEmailTo_entry, sendEmail_display_window):
        msg = EmailMessage()
        msg['Subject'] = 'Your bill '
        msg['From'] = "sant.vihangam@gmail.com"
        msg['To'] = "deo_santanurag@mail.com"  # receiver email
        global x
        file_name = "..\\Library_Stock\\Invoices\\2021\\2.pdf"
        msg.set_content('This is your Total bill\nyour Reference.No is: Bill')
        with open(file_name, 'rb') as content_file:
            content = content_file.read()

        msg.add_attachment(content, maintype='application', subtype='octet-stream', filename=file_name)
        qsend = messagebox.askyesno("Billing System", "Do you want to send the bill?")
        if qsend > 0:
            with smtplib.SMTP_SSL('smtp.gmail.com', 465) as smtp:
                smtp.login("sant.vihangam@gmail.com", "Password@123")
                smtp.send_message(msg)
            qsmsg = messagebox.showinfo("Information", "Bill send successfully")
        else:
            qnmsg = messagebox.showinfo("Information", "Bill not send")

