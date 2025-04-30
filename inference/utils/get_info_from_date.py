################ LICENSE ######################################
# This software is Copyright © 2025 The Regents of the University of California.
# All Rights Reserved. Permission to copy, modify, and distribute this software and its documentation
# for educational, research and non-profit purposes, without fee, and without a written agreement is
# hereby granted, provided that the above copyright notice, this paragraph and the following three paragraphs
# appear in all copies. Permission to make commercial use of this software may be obtained by contacting:
#
# Office of Innovation and Commercialization 9500 Gilman Drive, Mail Code 0910 University of California La Jolla, CA 92093-0910 innovation@ucsd.edu
# This software program and documentation are copyrighted by The Regents of the University of California. The software program and documentation are
# supplied “as is”, without any accompanying services from The Regents. The Regents does not warrant that the operation of the program will
# be uninterrupted or error-free. The end-user understands that the program was developed for research purposes and is advised not to rely exclusively on the program for any reason.
#
# IN NO EVENT SHALL THE UNIVERSITY OF CALIFORNIA BE LIABLE TO ANY PARTY FOR DIRECT, INDIRECT, SPECIAL,
# INCIDENTAL, OR CONSEQUENTIAL DAMAGES, INCLUDING LOST PROFITS, ARISING OUT OF THE USE OF THIS SOFTWARE
# AND ITS DOCUMENTATION, EVEN IF THE UNIVERSITY OF CALIFORNIA HAS BEEN ADVISED OF THE POSSIBILITY OF SUCH
# DAMAGE. THE UNIVERSITY OF CALIFORNIA SPECIFICALLY DISCLAIMS ANY WARRANTIES, INCLUDING, BUT NOT LIMITED TO,
# THE IMPLIED WARRANTIES OF MERCHANTABILITY AND FITNESS FOR A PARTICULAR PURPOSE. THE SOFTWARE PROVIDED HEREUNDER
# IS ON AN “AS IS” BASIS, AND THE UNIVERSITY OF CALIFORNIA HAS NO OBLIGATIONS TO PROVIDE MAINTENANCE, SUPPORT,
# UPDATES, ENHANCEMENTS, OR MODIFICATIONS.
################################################################

def get_info_from_date(date):
    yyyy = str(date)[:4]
    mm = str(date)[5:7]
    dd = str(date)[8:10]
    if yyyy == "2020" and mm in ["09", "10", "11", "12"]:
        winter_season = "20-21"
    if yyyy == "2021" and mm in ["01", "02", "03", "04"]:
        winter_season = "20-21"
    if yyyy == "2021" and mm in ["09", "10", "11", "12"]:
        winter_season = "21-22"
    if yyyy == "2022" and mm in ["01", "02", "03", "04"]:
        winter_season = "21-22"
    if yyyy == "2022" and mm in ["09", "10", "11", "12"]:
        winter_season = "22-23"
    if yyyy == "2023" and mm in ["01", "02", "03", "04"]:
        winter_season = "22-23"
    return yyyy, mm, dd, winter_season

